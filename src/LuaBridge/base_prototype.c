#include <Python.h>
#include <structmember.h>
#include <stddef.h>

typedef struct {
    PyObject_HEAD
    PyObject *dict;
    PyObject *name;
    PyObject *display_name;
} BasePrototype;

static int init(BasePrototype *self, PyObject *args, PyObject *kwds)
{
    PyObject *name = NULL;
    PyObject *display_name = NULL;

    static char *kwlist[] = {"name", "display_name", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "UU", kwlist, &name, &display_name))
        return -1;

    Py_INCREF(name);
    Py_INCREF(display_name);
    self->name = name;
    self->display_name = display_name;

    return 0;
}

static void dealloc(BasePrototype *self)
{
    Py_XDECREF(self->name);
    Py_XDECREF(self->display_name);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyMemberDef members[] = {
    {"name", T_OBJECT_EX, offsetof(BasePrototype, name), 0, "prototype name"},
    {"display_name", T_OBJECT_EX, offsetof(BasePrototype, display_name), 0, "prototype display name"},
    {NULL}  // sentinel
};

static PyMethodDef methods[] = {
    {NULL}  // Sentinel
};

PyTypeObject BasePrototype_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "LuaBridge.BasePrototype",
    .tp_basicsize = sizeof(BasePrototype),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "The Base Prototype",
    .tp_members = members,
    .tp_methods = methods,
    .tp_init = (initproc)init,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor)dealloc,
    .tp_dictoffset = offsetof(BasePrototype, dict)
};
