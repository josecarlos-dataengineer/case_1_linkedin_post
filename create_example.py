import sys
sys.path.append(r"C:\Users\SALA443\Desktop\linkedin_posts\linkedin_post\Lib\site-packages")
# Sessão 1: Importação das bibliotecas
import datetime
import pandas as pd
import pyodbc
import random
import uuid

# Sessão 2: Criação do dataframe de exemplo
clientes = {'id':[1,2,3,4,5,6,7,8,9,10],
            'nome':['Maria','Julia','Paulo','Luiz','Katia','José','Indiana','Antonio','Manuela','Pedro'],
            'idade':[50,25,62,18,62,82,32,45,74,61],
            'Estado':['SP','MG','RJ','PA','MA','RS','SP','MG','SP','MG']
            }

operacoes = {'id':[1,2,3,4,5,6],'tipo':['compra','compra','compra','compra','troca','devolução']}

canal_de_venda = {'id':[1,2,3],'canal':['WhatsApp','Loja','Ativo_Telemarketing']}

uuid.uuid4().hex[:8]

data = []

#número de vezes que o for será feito
size = 100
def carrega_lista():
        
        for n in range(len(clientes['id'])-1):
    
            cliente = clientes['nome'][n]
            idade = clientes['idade'][n]
            estado = clientes['Estado'][n]
            rand = random.randint(0,5)
            rand2 = random.randint(0,2)
            operacao = operacoes['tipo'][rand]
            quantidade = 1
            canal = canal_de_venda['canal'][rand2]
            data_evento = random.randint(1,28)
            mes_evento = random.randint(1,12)
            data_operacao = datetime.date(2023,mes_evento,data_evento)
            data_operacao = data_operacao.strftime('%Y-%m-%d')
            data_ = data_operacao
            data.append([cliente,idade,estado,operacao,quantidade,canal,data_])
             
n = 0
while n <= size:
    carrega_lista()
    n += 1   

# Conversão da lista de listas para Pandas Dataframe
df = pd.DataFrame.from_records(data=data, columns=['nome','idade','estado','operacao','quantidade','canal_venda','data_'])


# Conexão com o banco de dados *Aqui está sendo usado SQL Server, mas vc pode ajustar a 
# conn para o banco de sua preferência
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER=DESKTOP-DD8P4JN;DATABASE=estudos;UID=sa;PWD=jotace007')

cursor = conn.cursor()

for index, row in df.iterrows():
     cursor.execute("INSERT INTO dbo.index_teste (nome,idade,estado,operacao,quantidade,canal_venda,[data_]) values(?,?,?,?,?,?,?)", (row.nome, row.idade, row.estado, row.operacao, row.quantidade, row.canal_venda, row.data_))

conn.commit()
cursor.close()



