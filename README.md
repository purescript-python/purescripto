# Purescripto

PureScript, Python, support since Python 3.5.

`pspy` is provided to meet the interface of `spago`.

This requires the installation of [PureScript Python](https://github.com/thautwarm/purescript-python).

## Basic Usage

```bash
sh> pspy --init # initialize PSPY configure. PLEASE do this after `spago init`.
sh> pspy # build a project
sh> pspy --run # run built python package
sh> pspy --update # build and update Python FFI dependencies
```

Default output python package is the name of your PureScript project, i.e.,
project `xxx` produces a python package `xxx` in in directory `xxx/xxx`,
and you can add a `xxx/setup.py` to package Python modules and publish it to PyPI.
 

## `pure-py.json`

This is the default configuration.

```python
{
  "corefn-dir": "output",
  "entry-module": "Main",
  "index-mirror": "default",
  "pspy-blueprint": "pspy-blueprint",
  "spago": "spago"
}
```

It's designed for cases of making very complex extensions and very rare corner cases,
in most cases you're not expected to change it.

The details of `pure-py.json` will be added here when I have bandwidth.
