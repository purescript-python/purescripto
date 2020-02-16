# Purescripto

PureScript, Python, support since Python 3.5.

`pspy` is provided to meet the interface of `spago`.

This requires the installation of [PureScript Python](https://github.com/thautwarm/purescript-python).

```bash
sh> pspy # build a project
sh> pspy --run # run built python package  
```

Default output python package is the name of your PureScript project, i.e.,
project `xxx` produces a python package `xxx` in in directory `xxx/xxx`,
and you can add a `xxx/setup.py` to package Python modules and publish it to PyPI.
  
Currently I'm working on removing code generation for unused PureScript library,
and test the purescript-python compiler and this python wrapper.
  