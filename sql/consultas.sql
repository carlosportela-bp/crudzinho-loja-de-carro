-- Comandos SQL equivalentes ao que o sistema faz (core/views.py)
-- Rodar no banco loja_carros, depois do schema.sql e do dados.sql.
-- As consultas do dashboard (MIN, MAX, GROUP BY, HAVING, SUBQUERY, JOIN) estão em sql/dashboard.sql.
-- O arquivo pode ser executado inteiro, de cima para baixo: ele cria, consulta,
-- altera e no final exclui os próprios registros de exemplo.

-- ============================================================
-- VENDEDORES
-- ============================================================

-- Cadastrar
INSERT INTO vendedores (nome, numero_vendas) VALUES ('Vendedor Exemplo', 0);

-- Consultar
SELECT * FROM vendedores ORDER BY nome;

-- Filtro: busca por nome
SELECT * FROM vendedores WHERE nome ILIKE '%exemplo%' ORDER BY nome;

-- Atualizar
UPDATE vendedores SET numero_vendas = 1 WHERE nome = 'Vendedor Exemplo';

-- ============================================================
-- ESTOQUE  (tipo_veiculo: 1 = Carro, 2 = Moto, 3 = Caminhonete)
-- ============================================================

-- Cadastrar
INSERT INTO estoque (marca, modelo, ano, tipo_veiculo, preco, consignado)
VALUES ('Fiat', 'Uno Way', 2019, 1, 39900.00, FALSE);

-- Consultar
SELECT * FROM estoque ORDER BY id_carro;

-- Filtro: por tipo
SELECT * FROM estoque WHERE tipo_veiculo = 1 ORDER BY id_carro;

-- Filtro: só consignados
SELECT * FROM estoque WHERE consignado = TRUE ORDER BY id_carro;

-- Filtro: tipo e consignado juntos
SELECT * FROM estoque WHERE tipo_veiculo = 1 AND consignado = FALSE ORDER BY id_carro;

-- Atualizar (o último veículo cadastrado)
UPDATE estoque SET consignado = TRUE WHERE id_carro = (SELECT MAX(id_carro) FROM estoque);

-- ============================================================
-- VENDAS  (carros_vendas liga vendedores e estoque)
-- ============================================================

-- Cadastrar: idvendedores e id_carro precisam existir nas outras tabelas
INSERT INTO carros_vendas (idvendedores, id_carro, data_venda, valor_venda)
VALUES (
    (SELECT id FROM vendedores WHERE nome = 'Vendedor Exemplo'),
    (SELECT MAX(id_carro) FROM estoque),
    CURRENT_DATE,
    38500.00
);

-- Consultar com JOIN: dados das 3 tabelas juntos
SELECT cv.token_venda, cv.data_venda, cv.valor_venda, v.nome AS vendedor,
       e.id_carro, e.marca, e.modelo, e.tipo_veiculo, e.consignado
FROM carros_vendas cv
JOIN vendedores v ON v.id = cv.idvendedores
JOIN estoque e    ON e.id_carro = cv.id_carro
ORDER BY cv.token_venda DESC;

-- Filtro: vendas de um vendedor
SELECT cv.token_venda, v.nome AS vendedor, e.id_carro, e.tipo_veiculo
FROM carros_vendas cv
JOIN vendedores v ON v.id = cv.idvendedores
JOIN estoque e    ON e.id_carro = cv.id_carro
WHERE v.nome = 'Vendedor Exemplo';

-- Filtro: vendas por tipo de veículo (coluna de outra tabela, via JOIN)
SELECT cv.token_venda, v.nome AS vendedor, e.id_carro, e.tipo_veiculo
FROM carros_vendas cv
JOIN vendedores v ON v.id = cv.idvendedores
JOIN estoque e    ON e.id_carro = cv.id_carro
WHERE e.tipo_veiculo = 1;

-- Atualizar: trocar o veículo da venda mais recente
UPDATE carros_vendas
SET id_carro = (SELECT MAX(id_carro) FROM estoque)
WHERE token_venda = (SELECT MAX(token_venda) FROM carros_vendas);

-- ============================================================
-- CONSULTAS EXTRAS (relatórios)
-- ============================================================

-- Quantidade de vendas por vendedor
SELECT v.nome, COUNT(cv.token_venda) AS total_vendas
FROM vendedores v
LEFT JOIN carros_vendas cv ON cv.idvendedores = v.id
GROUP BY v.id, v.nome
ORDER BY total_vendas DESC;

-- Veículos que ainda não foram vendidos
SELECT e.*
FROM estoque e
LEFT JOIN carros_vendas cv ON cv.id_carro = e.id_carro
WHERE cv.token_venda IS NULL;

-- Chave estrangeira na prática: este DELETE falha enquanto o Vendedor Exemplo tiver vendas
-- (ERRO: ... viola restrição de chave estrangeira "carros_vendas_idvendedores_fkey")
-- DELETE FROM vendedores WHERE nome = 'Vendedor Exemplo';

-- ============================================================
-- EXCLUIR (ordem importa: primeiro a venda, depois veículo e vendedor)
-- ============================================================

DELETE FROM carros_vendas
WHERE idvendedores = (SELECT id FROM vendedores WHERE nome = 'Vendedor Exemplo');

DELETE FROM estoque WHERE id_carro = (SELECT MAX(id_carro) FROM estoque);

DELETE FROM vendedores WHERE nome = 'Vendedor Exemplo';
