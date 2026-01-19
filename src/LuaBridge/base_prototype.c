#include <Python.h>

typedef struct {
    PyObject_HEAD
    PyObject *type;
    PyObject *name;
} BasePrototype;

static int init(BasePrototype *self, PyObject *args, PyObject *kwds)
{
    PyObject *type = NULL;
    PyObject *name = NULL;

    static char *kwlist[] = {"type", "name", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "UU", kwlist, &type, &name))
        return -1;

    if (PyObject_SetAttrString((PyObject *)self, "type", type) < 0)
        return -1;
    if (PyObject_SetAttrString((PyObject *)self, "name", name) < 0)
        return -1;

    Py_INCREF(type);
    Py_INCREF(name);
    self->type = type;
    self->name = name;

    return 0;
}

static void dealloc(BasePrototype *self)
{
    Py_XDECREF(self->type);
    Py_XDECREF(self->name);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyMethodDef methods[] = {
    {NULL}  // Sentinel
};

PyTypeObject BasePrototype_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "LuaBridge.BasePrototype",
    .tp_basicsize = sizeof(BasePrototype),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "The Base Prototype",
    .tp_methods = methods,
    .tp_init = (initproc)init,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor)dealloc
};
