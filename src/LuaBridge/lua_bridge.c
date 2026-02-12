#include <Python.h>

#include "base_prototype.h"
#include "lua_sandbox.h"
#include "prototype_definition.h"

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
    if (PyType_Ready(&LuaSandbox_Type) < 0)
        return NULL;
    if (PyType_Ready(&PrototypeDefinition_Type) < 0)
        return NULL;

    Py_INCREF(&BasePrototype_Type);
    if (PyModule_AddObject(m, "BasePrototype", (PyObject *)&BasePrototype_Type) < 0)
    {
        Py_DECREF(&BasePrototype_Type);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&LuaSandbox_Type);
    if (PyModule_AddObject(m, "LuaSandbox", (PyObject *)&LuaSandbox_Type) < 0)
    {
        Py_DECREF(&LuaSandbox_Type);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&PrototypeDefinition_Type);
    if (PyModule_AddObject(m, "PrototypeDefinition", (PyObject *)&PrototypeDefinition_Type) < 0) 
    {
        Py_DECREF(&PrototypeDefinition_Type);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
