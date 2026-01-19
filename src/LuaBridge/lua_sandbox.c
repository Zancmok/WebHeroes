#include <Python.h>

typedef struct {
    PyObject_HEAD
} LuaSandbox;

static int init(LuaSandbox *self, PyObject *args, PyObject *kwds)
{ return 0; }

static void dealloc(LuaSandbox *self)
{
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyMethodDef methods[] = {
    {NULL}  // Sentinel
};

PyTypeObject LuaSandbox_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "LuaBridge.LuaSandbox",
    .tp_basicsize = sizeof(LuaSandbox),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "The Lua Sandbox",
    .tp_methods = methods,
    .tp_init = (initproc)init,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor)dealloc
};
