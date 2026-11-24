-- Consultas do Dashboard (as mesmas que o sistema executa em core/dashboard.py)
-- Rodar no banco loja_carros depois do schema.sql e do dados.sql.
--
-- Onde cada recurso obrigatório aparece:
--   MIN       -> 2, 3, 9, 10
--   MAX       -> 1, 3, 9, 10
--   GROUP BY  -> 4, 5, 6, 7, 8, 9, 10
--   HAVING    -> 7, 9
--   SUBQUERY  -> 1, 2, 3, 8, 9, 10
--   JOIN      -> 1, 2, 4, 5, 6, 7, 9

-- ============================================================
-- KPIs
-- ============================================================

-- KPI: faturamento total, quantidade de vendas e ticket médio
SELECT COUNT(*)                      AS total_vendas,
       COALESCE(SUM(valor_venda), 0) AS faturamento,
       COALESCE(AVG(valor_venda), 0) AS ticket_medio
FROM carros_vendas;

-- 1) KPI: maior venda (MAX + SUBQUERY + JOIN)
SELECT cv.valor_venda,
       cv.data_venda,
       v.nome                     AS vendedor,
       e.marca || ' ' || e.modelo AS veiculo
FROM carros_vendas cv
JOIN vendedores v ON v.id = cv.idvendedores
JOIN estoque e    ON e.id_carro = cv.id_carro
WHERE cv.valor_venda = (SELECT MAX(valor_venda) FROM carros_vendas)
LIMIT 1;

-- 2) KPI: menor venda (MIN + SUBQUERY + JOIN)
SELECT cv.valor_venda,
       cv.data_venda,
       v.nome                     AS vendedor,
       e.marca || ' ' || e.modelo AS veiculo
FROM carros_vendas cv
JOIN vendedores v ON v.id = cv.idvendedores
JOIN estoque e    ON e.id_carro = cv.id_carro
WHERE cv.valor_venda = (SELECT MIN(valor_venda) FROM carros_vendas)
LIMIT 1;

-- 3) KPI: veículos disponíveis, valor parado em estoque e faixa de preço
--    (MIN + MAX + SUBQUERY com NOT IN)
SELECT COUNT(*)                AS quantidade,
       COALESCE(SUM(preco), 0) AS valor_total,
       MIN(preco)              AS mais_barato,
       MAX(preco)              AS mais_caro
FROM estoque
WHERE id_carro NOT IN (SELECT id_carro FROM carros_vendas);

-- 4) KPI: vendedor destaque (JOIN + GROUP BY)
SELECT v.nome,
       COUNT(cv.token_venda) AS vendas,
       SUM(cv.valor_venda)   AS faturamento
FROM vendedores v
JOIN carros_vendas cv ON cv.idvendedores = v.id
GROUP BY v.id, v.nome
ORDER BY faturamento DESC
LIMIT 1;

-- ============================================================
-- GRÁFICOS
-- ============================================================

-- Gráfico de linhas: faturamento por mês (GROUP BY)
SELECT TO_CHAR(DATE_TRUNC('month', data_venda), 'MM/YYYY') AS mes,
       COUNT(*)         AS vendas,
       SUM(valor_venda) AS faturamento
FROM carros_vendas
GROUP BY DATE_TRUNC('month', data_venda)
ORDER BY DATE_TRUNC('month', data_venda);

-- 5) Gráfico de barras: faturamento por vendedor (LEFT JOIN + GROUP BY)
--    O LEFT JOIN faz aparecer também o vendedor que ainda não vendeu (com 0).
SELECT v.nome,
       COUNT(cv.token_venda)            AS vendas,
       COALESCE(SUM(cv.valor_venda), 0) AS faturamento
FROM vendedores v
LEFT JOIN carros_vendas cv ON cv.idvendedores = v.id
GROUP BY v.id, v.nome
ORDER BY faturamento DESC;

-- 6) Gráfico de rosca: vendas por tipo de veículo (JOIN + GROUP BY)
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

-- 7) Gráfico de barras horizontais: marcas com 2 ou mais vendas (JOIN + GROUP BY + HAVING)
SELECT e.marca,
       COUNT(*)            AS vendas,
       SUM(cv.valor_venda) AS faturamento
FROM carros_vendas cv
JOIN estoque e ON e.id_carro = cv.id_carro
GROUP BY e.marca
HAVING COUNT(*) >= 2
ORDER BY vendas DESC, e.marca;

-- ============================================================
-- TABELAS
-- ============================================================

-- 8) Média de faturamento por vendedor (SUBQUERY no FROM + GROUP BY)
SELECT COALESCE(AVG(total_vendedor), 0) AS media
FROM (SELECT SUM(valor_venda) AS total_vendedor
      FROM carros_vendas
      GROUP BY idvendedores) AS totais;

-- 9) Vendedores acima da média (JOIN + GROUP BY + HAVING com SUBQUERY + MIN/MAX)
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

-- 10) Estoque disponível por tipo: MIN, MAX e média de preço
--     (GROUP BY + SUBQUERY correlacionada com NOT EXISTS)
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
