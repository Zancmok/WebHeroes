#include <Python.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

typedef struct {
    PyObject_HEAD
} LuaSandbox;

static int LuaSandbox_init(LuaSandbox *self, PyObject *args, PyObject *kwds)
{
    return 0;
}

static void LuaSandbox_dealloc(LuaSandbox *self)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyMethodDef LuaSandbox_methods[] = {
    {NULL}  // Sentinel
};

static PyTypeObject LuaSandbox_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "LuaBridge.LuaSandbox",
    .tp_basicsize = sizeof(LuaSandbox),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "LuaSandbox class wrapping Lua VM",
    .tp_methods = LuaSandbox_methods,
    .tp_init = (initproc)LuaSandbox_init,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor)LuaSandbox_dealloc,
};

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

    if (PyType_Ready(&LuaSandbox_Type) < 0)
        return NULL;

    Py_INCREF(&LuaSandbox_Type);
    if (PyModule_AddObject(m, "LuaSandbox", (PyObject *)&LuaSandbox_Type) < 0) {
        Py_DECREF(&LuaSandbox_Type);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
