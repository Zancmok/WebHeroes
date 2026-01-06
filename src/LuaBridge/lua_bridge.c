#include <Python.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

int sandboxAmount = 0;
lua_State *sandboxes = NULL;

void openLuaSandbox(PyObject *name)
{
    lua_State *L = lua_open();

    if (!L)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create Lua state");
        return;
    }

    sandboxAmount++;
    sandboxes = (lua_State*)realloc(sandboxes, sizeof(lua_State*) * sandboxAmount);
    sandboxes[sandboxAmount - 1] = L;
}

static PyMethodDef lua_bridge_module_methods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef lua_bridge_module = {
    PyModuleDef_HEAD_INIT,
    "LuaBridge",
    NULL,
    -1,
    lua_bridge_module_methods
};

PyMODINIT_FUNC PyInit_LuaBridge(void)
{
    return PyModule_Create(&lua_bridge_module);
}
