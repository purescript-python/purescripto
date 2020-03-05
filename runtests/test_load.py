from purescripto.rts import META_ENV
from purescripto.topdown import load_topdown
from py_sexpr.stack_vm.emit import module_code
import zipfile
import io
filename = "C:/Users/twshe/Desktop/mydb/com-haskell/v0.1/purescript-cyberbrain/purescript_cyberbrain/Data/Show/pure.zip.py"
# filename = 'C:\\Users\\twshe\\Desktop\\mydb\\com-haskell\\v0.1\\purescript-cyberbrain\\purescript_cyberbrain\\Cyberbrain\\PyInstructions\\pure.zip.py'
zip = zipfile.ZipFile(filename)
file = io.StringIO(zip.read("source").decode("utf8"))
sexpr = load_topdown(file, META_ENV)
module_code(sexpr)