import fdb

def conn():
    conn = fdb.connect(
        host='127.0.0.1',
        database='C:/Ultra/Banco/liga.fdb',
        user='SYSDBA',
        password='masterkey',
        port=3050,
        charset='UNICODE_FSS'
    )
    return conn

def insertPrecoComprasParaProduto(codproduto,codproduto_clas,preco,operador):
    con = conn()
    cur = con.cursor()
    print("atualizando: cod: " + str(codproduto) + ' - clas: ' + str(codproduto_clas))
    sql = """
    insert into precos (
        precos_id,
        codproduto,
        codproduto_clas,
        preco,
        operador,
        dtaalter,
        dtavigencia
    ) values (
        (select max(precos_id) from precos)+1,
        """+str(codproduto)+""",
        """+str(codproduto_clas)+""",
        """+str(preco)+""",
        """+str(operador)+""",
        current_timestamp,
        current_date
    )
    """
    cur.execute(sql)
    con.commit()
    con.close()
    
def projetoProdutos():
    con = conn()
    cur = con.cursor()
    cur.execute("""
    select
        pp.projeto_id,
        pp.codproduto,
        pp.codproduto_clas,
        pp.unitario,
        (select preco from precos where codproduto = pp.codproduto and codproduto_clas = pp.codproduto_clas and dtaalter = max(p.dtaalter)),
        (select valor_custo_reposicao from custo_reposicao(pp.codproduto,pp.codproduto_clas, current_date,'S')) as custo_compra,
        pp.qtd,
        max(p.dtaalter) as dtaalter

    from projetos_produtos pp
        inner join projetos proj on (proj.projeto_id = pp.projeto_id)
        inner join precos p on (p.codproduto = pp.codproduto and p.codproduto_clas = pp.codproduto_clas)

    where
        proj.codstatus = '1'

    group by
        pp.projeto_id,
        pp.codproduto,
        pp.codproduto_clas,
        pp.unitario,
        pp.qtd

    order by 1
    """)
    return cur
    
def updateProjetoProdutos(projeto_id,codproduto,codproduto_clas,preco,qtd):
    con = conn()
    print("PROJETO_PRODUTOS: ", projeto_id, codproduto, codproduto_clas, preco)
    sql = """
    update projetos_produtos set 
        unitario = '""" + str(preco) + """',
        valor = '""" + str(round(float(preco)*float(qtd),2)) + """' ,
        total = '""" + str(round(float(preco)*float(qtd),2)) + """' ,
        custo_unitario = '""" + str(float(preco)) + """' ,
        total_custo = '""" + str(round(float(preco)*float(qtd),2)) + """'

    where 
        (select p.codstatus from projetos p where p.projeto_id = """ + str(projeto_id) + """) = '1' and
        projeto_id = """ + str(projeto_id) + """ and
        codproduto = """ + str(codproduto) + """ and
        codproduto_clas = """ + str(codproduto_clas)
        
    cur = con.cursor()
    cur.execute(sql)
    
    con.commit()
    con.close()