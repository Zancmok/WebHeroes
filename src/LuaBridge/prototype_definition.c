#include <Python.h>
#include <stddef.h>

#include "base_prototype.h"

typedef struct {
    PyObject_HEAD
    PyObject *dict;
    PyObject *prototype_definition;
    PyObject *synonym;
} PrototypeDefinition;

static int init(PrototypeDefinition *self, PyObject *args, PyObject *kwds)
{
    PyObject *prototype_definition = NULL;
    PyObject *synonym = NULL;

    static char *kwlist[] = {"prototype_definition", "synonym", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OU", kwlist, &prototype_definition, &synonym))
        return -1;

    if (!PyType_Check(prototype_definition))
    {
        PyErr_SetString(PyExc_TypeError, "Prototype_definition must be a type");
        return -1;
    }

    if (!PyObject_IsSubclass(prototype_definition, (PyObject *)&BasePrototype_Type))
    {
        PyErr_SetString(PyExc_TypeError, "prototype_definition must be a subclass of BasePrototype");
        return -1;
    }

    Py_INCREF(prototype_definition);
    Py_INCREF(synonym);
    self->prototype_definition = prototype_definition;
    self->synonym = synonym;

    return 0;
}

static void dealloc(PrototypeDefinition *self)
{
    Py_XDECREF(self->prototype_definition);
    Py_XDECREF(self->synonym);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyMethodDef methods[] = {
    {NULL}  // Sentinel
};

PyTypeObject PrototypeDefinition_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "LuaBridge.PrototypeDefinition",
    .tp_basicsize = sizeof(PrototypeDefinition),
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "The definition of a prototype",
    .tp_methods = methods,
    .tp_init = (initproc)init,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor)dealloc,
    .tp_dictoffset = offsetof(PrototypeDefinition, dict)
};
