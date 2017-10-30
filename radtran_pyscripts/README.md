#README.md  : AtmSimForP2IO_2017/radtran_pyscripts
====================

To run the atmospheric simulation for LSST, libradtran must be installed.
Its installation path must be defined in the variable $LIBRADTRANDIR

> echo $LIBRADTRANDIR
 
> /Users/dagoret/MacOSX/External/libRadtran/libRadtran-2.0.1


# create local directories
--------------------------------------------
- input/
- output/afglus

# and run :
--------------------
 
 >  python simulate\_transparency\_withpwvaod\_quantiles.py 

