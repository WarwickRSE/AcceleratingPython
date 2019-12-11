## Accelerating Python Workshop

This page contains all the code and suggestions for the WarwickRSE
"Accelerating Python" workshop.

Python is a convenient programming language, because it's available
readily on a lot of computers and has a very good library infrastructure.
But sometimes, expecially for "research" problems, it can be "too slow". 

This workshop first discusses what we mean by being "too slow", how to
find out, and how to know what speed to expect for a given problem. Then
we discuss all the options for making Python based code faster, while:
* Not having to stop doing research for weeks while you do it
* Not removing the convenient Python interface
* Not making your code too hard to run

The slides and description are available on our training pages at
https://warwick.ac.uk/research/rtp/sc/rse/training/acceleratingpython


### Other Tools

As well as Python itself (we use Python3), you might want to use
graphviz and gprof2dot to get pretty results at the profiling
part of the workshop. 

For the final part, where we discuss using C code linked in
to your Python code, you will need a C compiler. Any C compiler will
do - we work with GCC, which comes by default on Linux and OSX. 
On Windows, you might want to look into the
Windows 10 "Subsystem for Linux" (easiest), or on older Windows,
MinGW.
