# case_1_linkedin_post

Um dataset pequeno e simples aqui para exercitar a capacidade de questionar e analisar padrões de dados. <br>

```
SELECT TOP (10) [nome]
      ,[idade]
      ,[estado]
      ,[operacao]
      ,[quantidade]
      ,[canal_venda]
      ,[data_]
  FROM [estudos].[dbo].[index_teste]
```
 <br>
 
![alt text](imagens/exemplo.png)

A ideia aqui é responder a pergunta:  <br>
Qual faixa etária mais faz devoluções e trocas por estado e canal de compra?

Para responder essa pergunta e outras, vamos usar alguns recursos bem úteis e interassantes do SQL SERVER:  <br>
* CTE: "Especifica um conjunto de resultados nomeado temporário, conhecido como uma CTE (expressão de tabela comum). Ela é derivada de uma consulta simples e definida no escopo de execução de uma única instrução SELECT, INSERT, UPDATE, DELETE ou MERGE. Esta cláusula também pode ser usada em uma instrução CREATE VIEW como parte da instrução SELECT que a define. Uma expressão de tabela comum pode incluir referências a si mesma. É o que chamamos de expressão de tabela comum recursiva." [fonte site Microsoft](https://learn.microsoft.com/pt-br/sql/t-sql/queries/with-common-table-expression-transact-sql?view=sql-server-ver16) <br>
* Window Functions: Funções de agregação sobre partições definidas pelo usuário
* Builtin Functions: ROW_NUMBER, SUM, AVG, MAX

```
WITH agregacao AS (
SELECT 

	ROW_NUMBER() OVER (ORDER BY nome) AS SK,
	[nome],
	[idade],
	[estado],
	[operacao],
	[quantidade],	
	[canal_venda],
	[data_],
	SUM([quantidade]) OVER (PARTITION BY nome) AS qt_cliente,
	SUM([quantidade]) OVER (PARTITION BY estado,operacao,canal_venda) AS qt_estado_operacao_canal_venda,
	SUM([quantidade]) OVER (PARTITION BY estado,operacao) AS qt_estado_operacao,
	SUM([quantidade]) OVER (PARTITION BY operacao,canal_venda) AS qt_operacao_canal_venda,
	SUM([quantidade]) OVER (PARTITION BY operacao) AS qt_operacao

FROM [dbo].[index_teste]
)


,

analise_etaria AS (

SELECT
	[sk],	
	AVG([idade]) OVER (PARTITION BY [estado]) AS idade_media_estado,
	(SELECT AVG([idade]) FROM [dbo].[index_teste]) AS idade_media_BR,
	CASE
		WHEN [idade] < 30 THEN '18 +' 
		WHEN [idade] < 40 THEN '30 +' 
		WHEN [idade] < 50 THEN '40 +' 
		WHEN [idade] < 60 THEN '50 +' 
		WHEN [idade] < 70 THEN '60 +' 
		WHEN [idade] < 80 THEN '70 +' 
		ELSE '80 +' 
	END AS faixa_etaria

FROM agregacao)
,

OBT AS (

SELECT

	a.SK,
	a.[nome],
	a.[idade],
	a.[estado],
	a.[operacao],
	a.[quantidade],	
	a.[canal_venda],
	CASE 
		WHEN MONTH(a.[data_]) < 4 then 'T 1'
		WHEN MONTH(a.[data_]) < 7 then 'T 2'
		WHEN MONTH(a.[data_]) < 10 then 'T 3'
		WHEN MONTH(a.[data_]) < 13 then 'T 4' END AS trimestre,

	a.qt_cliente,
	a.qt_estado_operacao_canal_venda,
	a.qt_estado_operacao,
	a.qt_operacao_canal_venda,
	a.qt_operacao,
	b.idade_media_estado,
	b.idade_media_BR,
	b.faixa_etaria

FROM agregacao a
INNER JOIN analise_etaria b ON 
a.SK = b.sk),

--Qual faixa et�ria mais faz devolu��es e trocas por estado e canal de compra?
devolucoes_trocas_por_canal_estado as (
SELECT 

	estado, 
	faixa_etaria, 
	compra,
	canal_venda,
	devolu��o,
	troca, 
	CAST((devolu��o+troca) AS DECIMAL(5,2)) / CAST(COMPRA AS DECIMAL(5,2))*100 AS percentual_trocas_devolucoes

FROM (
    SELECT estado, faixa_etaria, operacao,canal_venda, quantidade
    FROM OBT
	WHERE trimestre IN ('T 1','T 2','T 3','T 4')


) AS SourceTable
PIVOT  
(  
    SUM(quantidade)  
    FOR   
    operacao   

    IN ( [compra], [devolu��o],[troca])  
) AS pvt


)

	SELECT 
	
		TOP 10 * 
	
	FROM  devolucoes_trocas_por_canal_estado
	
	ORDER BY 
		percentual_trocas_devolucoes DESC
```
