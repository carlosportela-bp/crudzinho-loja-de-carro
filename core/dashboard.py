"""Consultas SQL do dashboard.

Cada consulta é SQL puro, executado direto no PostgreSQL com connection.cursor().
O mesmo texto está em sql/dashboard.sql, para rodar no pgAdmin durante a apresentação.
"""

from django.db import connection

# ------------------------------------------------------------------
# KPIs
# ------------------------------------------------------------------

# KPI 1 e 2: faturamento total, quantidade de vendas e ticket médio
SQL_RESUMO_VENDAS = """
SELECT COUNT(*)                      AS total_vendas,
       COALESCE(SUM(valor_venda), 0) AS faturamento,
       COALESCE(AVG(valor_venda), 0) AS ticket_medio
FROM carros_vendas;
"""

# KPI 3: maior venda (MAX dentro de uma SUBQUERY + JOIN para buscar vendedor e veículo)
SQL_MAIOR_VENDA = """
SELECT cv.valor_venda,
       cv.data_venda,
       v.nome                     AS vendedor,
       e.marca || ' ' || e.modelo AS veiculo
FROM carros_vendas cv
JOIN vendedores v ON v.id = cv.idvendedores
JOIN estoque e    ON e.id_carro = cv.id_carro
WHERE cv.valor_venda = (SELECT MAX(valor_venda) FROM carros_vendas)
LIMIT 1;
"""

# KPI 4: menor venda (MIN dentro de uma SUBQUERY + JOIN)
SQL_MENOR_VENDA = """
SELECT cv.valor_venda,
       cv.data_venda,
       v.nome                     AS vendedor,
       e.marca || ' ' || e.modelo AS veiculo
FROM carros_vendas cv
JOIN vendedores v ON v.id = cv.idvendedores
JOIN estoque e    ON e.id_carro = cv.id_carro
WHERE cv.valor_venda = (SELECT MIN(valor_venda) FROM carros_vendas)
LIMIT 1;
"""

# KPI 5: veículos disponíveis (ainda não vendidos), valor parado em estoque e faixa de preço
SQL_ESTOQUE_DISPONIVEL = """
SELECT COUNT(*)                AS quantidade,
       COALESCE(SUM(preco), 0) AS valor_total,
       MIN(preco)              AS mais_barato,
       MAX(preco)              AS mais_caro
FROM estoque
WHERE id_carro NOT IN (SELECT id_carro FROM carros_vendas);
"""

# KPI 6: vendedor destaque (quem mais faturou)
SQL_VENDEDOR_DESTAQUE = """
SELECT v.nome,
       COUNT(cv.token_venda) AS vendas,
       SUM(cv.valor_venda)   AS faturamento
FROM vendedores v
JOIN carros_vendas cv ON cv.idvendedores = v.id
GROUP BY v.id, v.nome
ORDER BY faturamento DESC
LIMIT 1;
"""

# ------------------------------------------------------------------
# GRÁFICOS
# ------------------------------------------------------------------

# Gráfico de linhas: faturamento e vendas por mês
SQL_VENDAS_POR_MES = """
SELECT TO_CHAR(DATE_TRUNC('month', data_venda), 'MM/YYYY') AS mes,
       COUNT(*)         AS vendas,
       SUM(valor_venda) AS faturamento
FROM carros_vendas
GROUP BY DATE_TRUNC('month', data_venda)
ORDER BY DATE_TRUNC('month', data_venda);
"""

# Gráfico de barras: faturamento por vendedor (LEFT JOIN mostra também quem não vendeu)
SQL_FATURAMENTO_POR_VENDEDOR = """
SELECT v.nome,
       COUNT(cv.token_venda)            AS vendas,
       COALESCE(SUM(cv.valor_venda), 0) AS faturamento
FROM vendedores v
LEFT JOIN carros_vendas cv ON cv.idvendedores = v.id
GROUP BY v.id, v.nome
ORDER BY faturamento DESC;
"""

# Gráfico de rosca: vendas por tipo de veículo
SQL_VENDAS_POR_TIPO = """
SELECT CASE e.tipo_veiculo
           WHEN 1 THEN 'Carro'
           WHEN 2 THEN 'Moto'
           WHEN 3 THEN 'Caminhonete'
       END                 AS tipo,
       COUNT(*)            AS vendas,
       SUM(cv.valor_venda) AS faturamento
FROM carros_vendas cv
JOIN estoque e ON e.id_carro = cv.id_carro
GROUP BY e.tipo_veiculo
ORDER BY vendas DESC;
"""

# Gráfico de barras horizontais: marcas que venderam 2 ou mais veículos (HAVING)
SQL_MARCAS_MAIS_VENDIDAS = """
SELECT e.marca,
       COUNT(*)            AS vendas,
       SUM(cv.valor_venda) AS faturamento
FROM carros_vendas cv
JOIN estoque e ON e.id_carro = cv.id_carro
GROUP BY e.marca
HAVING COUNT(*) >= 2
ORDER BY vendas DESC, e.marca;
"""

# ------------------------------------------------------------------
# TABELAS
# ------------------------------------------------------------------

# Média de faturamento por vendedor (SUBQUERY no FROM)
SQL_MEDIA_POR_VENDEDOR = """
SELECT COALESCE(AVG(total_vendedor), 0) AS media
FROM (SELECT SUM(valor_venda) AS total_vendedor
      FROM carros_vendas
      GROUP BY idvendedores) AS totais;
"""

# Vendedores acima da média: JOIN + GROUP BY + HAVING com SUBQUERY + MIN/MAX por vendedor
SQL_VENDEDORES_ACIMA_DA_MEDIA = """
SELECT v.nome,
       COUNT(cv.token_venda) AS vendas,
       SUM(cv.valor_venda)   AS faturamento,
       MIN(cv.valor_venda)   AS menor_venda,
       MAX(cv.valor_venda)   AS maior_venda
FROM vendedores v
JOIN carros_vendas cv ON cv.idvendedores = v.id
GROUP BY v.id, v.nome
HAVING SUM(cv.valor_venda) > (
    SELECT AVG(total_vendedor)
    FROM (SELECT SUM(valor_venda) AS total_vendedor
          FROM carros_vendas
          GROUP BY idvendedores) AS totais
)
ORDER BY faturamento DESC;
"""

# Estoque disponível por tipo: MIN, MAX e média de preço (SUBQUERY com NOT EXISTS)
SQL_ESTOQUE_POR_TIPO = """
SELECT CASE e.tipo_veiculo
           WHEN 1 THEN 'Carro'
           WHEN 2 THEN 'Moto'
           WHEN 3 THEN 'Caminhonete'
       END            AS tipo,
       COUNT(*)       AS quantidade,
       MIN(e.preco)   AS menor_preco,
       MAX(e.preco)   AS maior_preco,
       AVG(e.preco)   AS preco_medio
FROM estoque e
WHERE NOT EXISTS (SELECT 1 FROM carros_vendas cv WHERE cv.id_carro = e.id_carro)
GROUP BY e.tipo_veiculo
ORDER BY e.tipo_veiculo;
"""


def consultar(sql):
    """Executa o SQL e devolve uma lista de dicionários (uma linha = um dicionário)."""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        colunas = [c[0] for c in cursor.description]
        return [dict(zip(colunas, linha)) for linha in cursor.fetchall()]


def consultar_um(sql):
    """Executa o SQL e devolve só a primeira linha (ou None se não houver)."""
    linhas = consultar(sql)
    return linhas[0] if linhas else None
