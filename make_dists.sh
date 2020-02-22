for PLAT in "win64" "linux64" "macosx_10_15" ; do
  for CPY in "35" "36" "37" "38" ; do
      export CPY=$CPY
      export PLAT=$PLAT
      python setup.py bdist_wheel
  done
done