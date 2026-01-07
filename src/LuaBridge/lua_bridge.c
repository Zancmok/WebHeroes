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

// Type definition for LuaSandbox class
static PyTypeObject LuaSandbox_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "lua_bridge.LuaSandbox",    // Name of the class
    sizeof(LuaSandbox),       // Size of the structure
    0,                        // tp_dealloc
    0,                        // tp_print
    0,                        // tp_getattr
    0,                        // tp_setattr
    0,                        // tp_compare
    0,                        // tp_repr
    0,                        // tp_as_number
    0,                        // tp_as_sequence
    0,                        // tp_as_mapping
    0,                        // tp_hash
    0,                        // tp_call
    0,                        // tp_str
    0,                        // tp_getattro
    0,                        // tp_setattro
    0,                        // tp_as_buffer
    Py_TPFLAGS_DEFAULT,       // tp_flags
    0,                        // tp_doc
    0,                        // tp_traverse
    0,                        // tp_clear
    0,                        // tp_richcompare
    0,                        // tp_weaklistoffset
    0,                        // tp_iter
    0,                        // tp_iternext
    LuaSandbox_methods,       // tp_methods
    0,                        // tp_members
    0,                        // tp_getset
    0,                        // tp_base
    0,                        // tp_dict
    0,                        // tp_descr_get
    0,                        // tp_descr_set
    0,                        // tp_dictoffset
    (initproc)LuaSandbox_init, // tp_init
    0,                        // tp_alloc
    0,                        // tp_new
    (destructor)LuaSandbox_dealloc, // tp_dealloc
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

    Py_INCREF(&LuaSandbox_Type);
    if (PyModule_AddObject(m, "LuaSandbox", (PyObject *)&LuaSandbox_Type) < 0) {
        Py_DECREF(&LuaSandbox_Type);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
