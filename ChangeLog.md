## v0.6

### 2/23/2020

1. Suppressing warning of using `is` for CPython 3.8+.
   
   References:
   - https://github.com/purescript-python/purescript-python/issues/9
   - https://bugs.python.org/issue34850
 
 2. Workaround metadata errors, PureScript compiler produces code with `lineno=0`:
   
    References:
    - https://github.com/purescript-python/purescript-python/issues/8
 