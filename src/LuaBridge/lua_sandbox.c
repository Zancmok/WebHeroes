#include <Python.h>
#include <string.h>
#include <stddef.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

#include "prototype_definition.h"

typedef struct {
    PyObject_HEAD
    PyObject *dict;
    PyObject *prototypes;
    PyObject *mod_paths;
} LuaSandbox;

static int init(LuaSandbox *self, PyObject *args, PyObject *kwds)
{
    PyObject *prototypes = NULL, *mod_paths = NULL;
    static char *kwlist[] = {"prototypes", "mod_paths", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO", kwlist, &prototypes, &mod_paths))
        return -1;

    if (!PyList_Check(prototypes) || !PyList_Check(mod_paths)) {
        PyErr_SetString(PyExc_TypeError, "prototypes and mod_paths must be lists");
        return -1;
    }

    Py_INCREF(prototypes);
    Py_INCREF(mod_paths);
    self->prototypes = prototypes;
    self->mod_paths = mod_paths;
    return 0;
}

static void dealloc(LuaSandbox *self)
{
    Py_XDECREF(self->prototypes);
    Py_XDECREF(self->mod_paths);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

// --- safe recursive table to dict conversion ---
static PyObject* create_pclass(LuaSandbox *self, lua_State *L)
{
    if (!lua_istable(L, -1)) {
        PyErr_SetString(PyExc_RuntimeError, "Expected Lua table on stack");
        return NULL;
    }

    PyObject *py_dict = PyDict_New();
    if (!py_dict) return NULL;

    lua_pushnil(L);
    while (lua_next(L, -2) != 0) {
        const char *key = lua_tostring(L, -2);
        if (!key) key = "unknown_key";

        if (strcmp(key, "type") == 0)
        {
            lua_pop(L, 1);
            continue;
        }

        PyObject *value = NULL;
        if (lua_isnil(L, -1)) { Py_INCREF(Py_None); value = Py_None; }
        else if (lua_isboolean(L, -1)) value = PyBool_FromLong(lua_toboolean(L, -1));
        else if (lua_isnumber(L, -1)) value = PyLong_FromLongLong((long long)lua_tointeger(L, -1));
        else if (lua_isstring(L, -1)) {
            size_t len;
            const char *s = lua_tolstring(L, -1, &len);
            value = PyUnicode_FromStringAndSize(s, len);
        }
        else if (lua_istable(L, -1)) value = create_pclass(self, L);
        else { Py_INCREF(Py_None); value = Py_None; }

        if (!value) { lua_pop(L, 1); Py_DECREF(py_dict); return NULL; }

        PyDict_SetItemString(py_dict, key, value);
        Py_DECREF(value);
        lua_pop(L, 1); // pop value
    }

    // Get the type
    lua_getfield(L, -1, "type");
    const char *type = lua_tostring(L, -1);
    if (!type) {
        Py_DECREF(py_dict);
        lua_pop(L, 1);
        PyErr_SetString(PyExc_RuntimeError, "Lua table missing 'type'");
        return NULL;
    }

    PyObject *prototype_definition = NULL;
    Py_ssize_t proto_len = PyList_Size(self->prototypes);
    for (Py_ssize_t i = 0; i < proto_len; i++) {
        PrototypeDefinition *item = PyList_GetItem(self->prototypes, i);
        const char *synonym_str = PyUnicode_AsUTF8(item->synonym);
        if (synonym_str && strcmp(synonym_str, type) == 0) {
            prototype_definition = item->prototype_definition;
            break;
        }
    }

    if (!prototype_definition || !PyCallable_Check(prototype_definition)) {
        Py_DECREF(py_dict);
        lua_pop(L, 1);
        PyErr_Format(PyExc_RuntimeError, "No callable prototype found for type '%s'", type);
        return NULL;
    }

    PyObject *args = PyTuple_New(0);
    PyObject *pclass = PyObject_Call(prototype_definition, args, py_dict);
    Py_DECREF(args);

    lua_pop(L, 1); // pop type
    Py_XDECREF(py_dict);

    return pclass;
}

static PyObject* run(LuaSandbox *self, PyObject *args, PyObject *kwds)
{
    lua_State *L = luaL_newstate();
    if (!L)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create a Lua state");
        return NULL;
    }
    luaL_openlibs(L);

    Py_ssize_t len = PyList_Size(self->mod_paths);

    // --- Information stage: load info.lua ---
    for (Py_ssize_t i = 0; i < len; i++)
    {
        PyObject *item = PyList_GetItem(self->mod_paths, i);
        const char* mod_name = PyUnicode_AsUTF8(item);
        if (!mod_name) { lua_close(L); return NULL; }

        char filepath[512];
        snprintf(filepath, sizeof(filepath), "BaseMods/%s/info.lua", mod_name);

        if (luaL_loadfile(L, filepath) != 0 || lua_pcall(L, 0, 0, 0) != 0)
        {
            PyErr_SetString(PyExc_RuntimeError, lua_tostring(L, -1));
            lua_close(L);
            return NULL;
        }
    }

    // --- Prepare Lua environment for data.lua ---
    lua_close(L);
    L = luaL_newstate();
    if (!L) { PyErr_SetString(PyExc_RuntimeError, "Failed to create Lua state"); return NULL; }
    luaL_openlibs(L);

    // Create global `data` table for Lua mods to extend
    lua_newtable(L);
    lua_setglobal(L, "data");

    // --- Setup data.raw and prototype tables ---
    lua_getglobal(L, "data");      // push data
    lua_newtable(L);                // data.raw

    Py_ssize_t prototype_type_amount = PyList_Size(self->prototypes);
    for (Py_ssize_t i = 0; i < prototype_type_amount; i++)
    {
        PrototypeDefinition *item = (PrototypeDefinition *)PyList_GetItem(self->prototypes, i);
        const char* synonym = PyUnicode_AsUTF8(item->synonym);

        lua_newtable(L);             // empty table for this prototype type
        lua_setfield(L, -2, synonym);
    }

    lua_setfield(L, -2, "raw");    // data.raw = {...}
    lua_pop(L, 1);                 // pop data


    // --- Load data.lua for each mod ---
    for (Py_ssize_t i = 0; i < len; i++)
    {
        PyObject *item = PyList_GetItem(self->mod_paths, i);
        const char* mod_name = PyUnicode_AsUTF8(item);
        if (!mod_name) { lua_close(L); return NULL; }

        char command[512];
        snprintf(command, sizeof(command), "package.path = 'BaseMods/%s/?.lua;' .. package.path", mod_name);
        luaL_dostring(L, command);

        char filepath[512];
        snprintf(filepath, sizeof(filepath), "BaseMods/%s/data.lua", mod_name);

        if (luaL_loadfile(L, filepath) != 0 || lua_pcall(L, 0, 0, 0) != 0)
        {
            PyErr_SetString(PyExc_RuntimeError, lua_tostring(L, -1));
            lua_close(L);
            return NULL;
        }
    }

    // --- Convert Lua tables to Python prototypes ---
    PyObject *py_list = PyList_New(0);

    lua_getglobal(L, "data");
    lua_getfield(L, -1, "raw");

    for (Py_ssize_t i = 0; i < prototype_type_amount; i++)
    {
        PrototypeDefinition *item = (PrototypeDefinition *)PyList_GetItem(self->prototypes, i);
        const char* synonym = PyUnicode_AsUTF8(item->synonym);

        lua_getfield(L, -1, synonym);
        if (!lua_istable(L, -1)) { lua_pop(L, 1); continue; }

        size_t list_len = lua_rawlen(L, -1);
        for (size_t j = 1; j <= list_len; j++)
        {
            lua_rawgeti(L, -1, j);

            PyObject *new_object = create_pclass(self, L);
            if (!new_object) { lua_close(L); Py_DECREF(py_list); return NULL; }

            PyList_Append(py_list, new_object);
            Py_DECREF(new_object);

            lua_pop(L, 1);
        }

        lua_pop(L, 1);
    }

    lua_pop(L, 2);  // pop raw and data
    lua_close(L);

    return py_list;
}

static PyMethodDef methods[] = {
    {"run", (PyCFunction)run, METH_VARARGS, ""},
    {NULL}
};

PyTypeObject LuaSandbox_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "LuaBridge.LuaSandbox",
    .tp_basicsize = sizeof(LuaSandbox),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "The Lua Sandbox",
    .tp_methods = methods,
    .tp_init = (initproc)init,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor)dealloc,
    .tp_dictoffset = offsetof(LuaSandbox, dict)
};
