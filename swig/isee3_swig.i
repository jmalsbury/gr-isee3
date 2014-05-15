/* -*- c++ -*- */

#define ISEE3_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "isee3_swig_doc.i"

%{
#include "isee3/square_ff.h"
%}


%include "isee3/square_ff.h"
GR_SWIG_BLOCK_MAGIC2(isee3, square_ff);
