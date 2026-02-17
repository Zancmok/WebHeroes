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
    PyObject *prototypes = NULL;
    PyObject *mod_paths = NULL;

    static char *kwlist[] = {"prototypes", "mod_paths", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO", kwlist, &prototypes, &mod_paths))
        return -1;

    if (!PyList_Check(prototypes))
    {
        PyErr_SetString(PyExc_TypeError, "Prototypes must be a list");
        return -1;
    }

    Py_ssize_t len;

    len = PyList_Size(prototypes);
    for (Py_ssize_t i = 0; i < len; i++)
    {
        PyObject *item = PyList_GetItem(prototypes, i);

        if (!PyObject_TypeCheck(item, &PrototypeDefinition_Type))
        {
            PyErr_SetString(PyExc_TypeError, "All prototypes must be instances of PrototypeDefinition");
            return -1;
        }
    }
    
    if (!PyList_Check(mod_paths))
    {
        PyErr_SetString(PyExc_TypeError, "mod_paths must be a list");
        return -1;
    }

    len = PyList_Size(mod_paths);
    for (Py_ssize_t i = 0; i < len; i++)
    {
        PyObject *item = PyList_GetItem(mod_paths, i);

        if (!PyUnicode_Check(item))
        {
            PyErr_SetString(PyExc_TypeError, "All items must be strings");
            return -1;
        }
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

static PyObject* run(LuaSandbox *self, PyObject *args, PyObject *kwds)
{
    lua_State *L = luaL_newstate();
    if (!L)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create a Lua state");
        return NULL;
    }

    Py_ssize_t len = PyList_Size(self->mod_paths);

    // Information stage
    for (Py_ssize_t i = 0; i < len; i++)
    {
        PyObject *item = PyList_GetItem(self->mod_paths, i);
        const char* mod_name = PyUnicode_AsUTF8(item);

        if (mod_name == NULL)
        {
            lua_close(L);

            return NULL;
        }

        char filepath[512];
        snprintf(filepath, sizeof(filepath), "BaseMods/%s/info.lua", mod_name);

        if (luaL_loadfile(L, filepath) != 0 || lua_pcall(L, 0, 0, 0) != 0)
        {
            const char* err = lua_tostring(L, -1);
            PyErr_SetString(PyExc_RuntimeError, err);

            lua_close(L);

            return NULL;
        }
    }   

    // Reopen a new Lua instance
    lua_close(L);
    L = luaL_newstate();
    if (!L)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create a Lua state");
        return NULL;
    }
    luaL_openlibs(L);

    // Make the data table
    lua_newtable(L);  // data
    lua_newtable(L);  // data.raw

    // Load prototypes
    Py_ssize_t prototype_type_amount = PyList_Size(self->prototypes);
    for (Py_ssize_t i = 0; i < prototype_type_amount; i++)
    {
        PrototypeDefinition *item = (PrototypeDefinition *)PyList_GetItem(self->prototypes, i);
        const char* synonym = PyUnicode_AsUTF8(item->synonym);

        lua_newtable(L);
        lua_setfield(L, -2, synonym);
    }

    lua_setfield(L, -2, "raw");
    lua_setglobal(L, "data");

    // Data stage
    for (Py_ssize_t i = 0; i < len; i++)
    {
        PyObject *item = PyList_GetItem(self->mod_paths, i);
        const char* mod_name = PyUnicode_AsUTF8(item);

        if (mod_name == NULL)
        {
            lua_close(L);

            return NULL;
        }

        char command[512];
        snprintf(command, sizeof(command), "package.path = 'BaseMods/%s/?.lua;' .. package.path", mod_name);
        luaL_dostring(L, command);

        char filepath[512];
        snprintf(filepath, sizeof(filepath), "BaseMods/%s/data.lua", mod_name);

        if (luaL_loadfile(L, filepath) != 0 || lua_pcall(L, 0, 0, 0) != 0)
        {
            const char* err = lua_tostring(L, -1);
            PyErr_SetString(PyExc_RuntimeError, err);

            lua_close(L);

            return NULL;
        }
    }

    // Return prototypes
    PyObject *py_list = PyList_New(0);

    lua_getglobal(L, "data");
    lua_getfield(L, -1, "raw");

    for (Py_ssize_t i = 0; i < prototype_type_amount; i++)
    {
        PrototypeDefinition *item = (PrototypeDefinition *)PyList_GetItem(self->prototypes, i);
        const char* synonym = PyUnicode_AsUTF8(item->synonym);

        lua_getfield(L, -1, synonym);

        size_t list_len = lua_rawlen(L, -1);
        for (size_t j = 1; j <= list_len; j++)
        {
            lua_rawgeti(L, -1, j);
            
            PyObject *py_dict = PyDict_New();
            lua_pushnil(L);

            while (lua_next(L, -2) != 0)
            {
                const char *key = lua_tostring(L, -2);

                // Add recursive magic

                lua_pop(L, 1);
            }

            Py_DECREF(py_dict);

            lua_pop(L, 1);
        }

        lua_pop(L, 1);
    }

    lua_pop(L, 2);
    lua_close(L);

    return py_list;
}

static PyMethodDef methods[] = {
    {"run", (PyCFunction)run, METH_VARARGS, ""},
    {NULL}  // Sentinel
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
