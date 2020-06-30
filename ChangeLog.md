## v0.8

### (Unreleased) v0.8.9(6/30/2020)
1. Cache the import of a purescript module, in order to avoid its re-import during 
   importing it for the first time.

## v0.6

### v0.6.2(2/23/2020)

1. Suppressing warning of using `is` for CPython 3.8+.
   
   References:
   - https://github.com/purescript-python/purescript-python/issues/9
   - https://bugs.python.org/issue34850
 
 2. Workaround metadata errors, PureScript compiler produces code with `lineno=0`:
   
    References:
    - https://github.com/purescript-python/purescript-python/issues/8
 
 
 3. Workaround for compating JavaScript incomplete arguments.
    
    References:
    - https://github.com/purescript-python/purescript-python/issues/10
   
### v0.6.3(2/24/2020)

1. `--update` will update currently used mirror
