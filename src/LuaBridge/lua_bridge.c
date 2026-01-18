#include <Python.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

#include "base_prototype.h"

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
    PyObject *m = PyModule_Create(&lua_bridge_module);
    if (!m)
        return NULL;
    if (PyType_Ready(&BasePrototype_Type) < 0)
        return NULL;

    Py_INCREF(&BasePrototype_Type);
    if (PyModule_AddObject(m, "BasePrototype", (PyObject *)&BasePrototype_Type) < 0) {
        Py_DECREF(&BasePrototype_Type);
        Py_DECREF(m);
        return NULL;
    }
    return m;
}
