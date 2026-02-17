#ifndef PROTOTYPE_DEFINITION_H
#define PROTOTYPE_DEFINITION_H

#include <Python.h>

extern PyTypeObject PrototypeDefinition_Type;

typedef struct {
    PyObject_HEAD
    PyObject *dict;
    PyObject *prototype_definition;
    PyObject *synonym;
} PrototypeDefinition;

#endif
