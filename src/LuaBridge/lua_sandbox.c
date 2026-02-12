#include <Python.h>
#include <stddef.h>

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
        PyErr_SetString(PyExc_TypeError, "Prototypes must be a list");
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
    Py_RETURN_NONE;
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
