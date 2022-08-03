from conn import *
import time

# import ctypes
# ctypes.windll.kernel32.FreeConsole()    

def precosParaCompras():
    con = projetoProdutos()
    for c in con.fetchall():
        if c[3] != c[5]:            
            if type(c[5]) == type(None):
                novo_preco = 0
            else:
                insertPrecoComprasParaProduto(c[1],c[2],c[5],1)
                updateProjetoProdutos(c[0],c[1],c[2],c[4],c[6])

while True:
    precosParaCompras()
    time.sleep(5)
    print("Verificando novas alterações.")
