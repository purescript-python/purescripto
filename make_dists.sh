for PLAT in "win64" "linux64" "macosx_10_15" ; do
    export PLAT=$PLAT
    python setup.py bdist_wheel
done