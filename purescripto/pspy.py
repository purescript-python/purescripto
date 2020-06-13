from purescripto.configure import pspy
from purescripto.installer import get_binary
from purescripto.template_setup import gen_setup, gen_init

def cmd_get_binary():
    import wisepy2
    wisepy2.wise(get_binary)()


def cmd_gen_setup():
    import wisepy2
    wisepy2.wise(gen_setup)()

def cmd_gen_init():
    import wisepy2
    wisepy2.wise(gen_init)()

def cmd_pspy():
    import wisepy2
    wisepy2.wise(pspy)()