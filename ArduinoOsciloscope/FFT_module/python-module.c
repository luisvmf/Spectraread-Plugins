//Copyright (c) 2024 Luís Victor Muller Fabris. Apache License.
#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <string.h>
#include <dirent.h> 
#include <time.h>
#include <sys/time.h>
#include "cmodule.c"



static PyObject* FFT_compute_call(PyObject* self,  PyObject *args) {
	int len;
	PyObject *obj;
	PyObject *objb;
	PyObject *iter;
	PyObject *iterb;
	PyObject *next;
	if (!PyArg_ParseTuple(args, "OOi",&obj,&objb,&len)) {
		return NULL;
	}
	double *xdata=(double*)malloc(len*sizeof(double));
	double *ydata=(double*)malloc(len*sizeof(double));
	int i=0;
	iter=PyObject_GetIter(obj);
	iterb=PyObject_GetIter(objb);
	if(!iter){
		return;
	}
	if(!iterb){
		return;
	}
	while(1){
		next=PyIter_Next(iter);
		if(!next){
			break;
		}
		if(i>=len){
			break;
		}
		double foo=PyFloat_AsDouble(next);
		xdata[i]=foo;
		i=i+1;
		Py_DECREF(next);// Prevent memory leak.
	}
	i=0;
	while(1){
		next=PyIter_Next(iterb);
		if(!next){
			break;
		}
		if(i>=len){
			break;
		}
		double foo=PyFloat_AsDouble(next);
		ydata[i]=foo;
		i=i+1;
		Py_DECREF(next);// Prevent memory leak.
	}
	double **result=FFT_get_frequency_spectrum(xdata,ydata,&len);


   PyObject *xlist = PyList_New(len);
    for (int i = 0; i < len; i++) {
        PyList_SET_ITEM(xlist, i, PyFloat_FromDouble(result[0][i]));
    }
   PyObject *ylist = PyList_New(len);
    for (int i = 0; i < len; i++) {
        PyList_SET_ITEM(ylist, i, PyFloat_FromDouble(result[1][i]));
    }
	free(result[0]);
	free(result[1]);
	free(result);
	return Py_BuildValue("OOi", xlist,ylist,len);
}
static char mmap_docs_FFT_compute[] =
   "FFT_compute(x[],y[],len): Compute FFT.";
static PyMethodDef FFT_compute_funcs[] = {
	{"FFT_compute", (PyCFunction)FFT_compute_call, METH_VARARGS, mmap_docs_FFT_compute},
	{ NULL, NULL, 0, NULL}
};

static struct PyModuleDef FFT_compute =
{
    PyModuleDef_HEAD_INIT,
    "FFT_compute", /* name of module */
    NULL,
    -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    FFT_compute_funcs
};
//void initfastmmapmq(void) {
//	//Py_InitModule3("FFT_compute", FFT_compute_funcs,"FFT_compute");
// 	return PyModule_Create(&Combinations);
//}
PyMODINIT_FUNC PyInit_FFT_compute(void)
{
    return PyModule_Create(&FFT_compute);
}
