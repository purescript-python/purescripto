for PLAT in "win64" "linux64" "macosx_10_15" ; do
  for CPY in "37" ; do
      export CPY=$CPY
      export PLAT=$PLAT
      python setup.py bdist_wheel
  done
done