#export PKG_CONFIG_PATH=$PWD/../../:$PKG_CONFIG_PATH
#export PATH=$PWD/../../Python/bin:$PATH&&export PYTHONPATH=$PWD/../../Python/lib/python2.7&&export PYTHONHOME=$PWD/../../Python/
#export LD_LIBRARY_PATH=$PWD/../../Python/lib
#$PWD/../../Python/bin/python setup.py install --home=./
python setup.py install --home=./
