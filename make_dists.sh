for PLAT in "win64" ; do
    export PLAT=$PLAT
    python setup.py bdist_wheel
done