-- Dados de exemplo da loja (dezembro/2025 a novembro/2026).
-- Rodar logo depois do sql/schema.sql: as vendas usam os ids 1, 2, 3...
-- gerados pelos INSERTs abaixo.

-- ============================================================
-- VENDEDORES
-- ============================================================
INSERT INTO vendedores (nome) VALUES
    ('Ana Souza'),        -- 1
    ('Bruno Lima'),       -- 2
    ('Carla Mendes'),     -- 3
    ('Diego Rocha'),      -- 4
    ('Eduarda Alves'),    -- 5
    ('Felipe Costa'),     -- 6
    ('Gabriela Nunes'),   -- 7
    ('Henrique Dias');    -- 8 (contratado agora, ainda sem vendas)

-- ============================================================
-- ESTOQUE  (tipo_veiculo: 1 = Carro, 2 = Moto, 3 = Caminhonete)
-- ============================================================
INSERT INTO estoque (marca, modelo, ano, tipo_veiculo, preco, consignado) VALUES
    ('Toyota',     'Corolla XEi',          2022, 1, 129900.00, FALSE),  -- 1
    ('Honda',      'Civic EXL',            2021, 1, 119900.00, FALSE),  -- 2
    ('Volkswagen', 'Polo Highline',        2023, 1,  98900.00, FALSE),  -- 3
    ('Chevrolet',  'Onix LT',              2022, 1,  76900.00, FALSE),  -- 4
    ('Fiat',       'Argo Drive',           2021, 1,  64900.00, TRUE),   -- 5
    ('Hyundai',    'HB20 Comfort',         2022, 1,  72900.00, FALSE),  -- 6
    ('Toyota',     'Yaris XL',             2023, 1,  94900.00, FALSE),  -- 7
    ('Volkswagen', 'Virtus Comfortline',   2022, 1,  99900.00, TRUE),   -- 8
    ('Chevrolet',  'Onix Plus Premier',    2023, 1, 104900.00, FALSE),  -- 9
    ('Fiat',       'Cronos Precision',     2022, 1,  82900.00, FALSE),  -- 10
    ('Honda',      'City EXL',             2023, 1, 117900.00, FALSE),  -- 11
    ('Renault',    'Kwid Zen',             2022, 1,  52900.00, TRUE),   -- 12
    ('Hyundai',    'Creta Limited',        2023, 1, 139900.00, FALSE),  -- 13
    ('Jeep',       'Renegade Longitude',   2022, 1, 124900.00, FALSE),  -- 14
    ('Toyota',     'Corolla Cross XRE',    2023, 1, 164900.00, FALSE),  -- 15
    ('Volkswagen', 'T-Cross Highline',     2023, 1, 149900.00, TRUE),   -- 16
    ('BMW',        '320i M Sport',         2021, 1, 239900.00, TRUE),   -- 17
    ('Chevrolet',  'Tracker Premier',      2023, 1, 142900.00, FALSE),  -- 18
    ('Fiat',       'Mobi Like',            2021, 1,  48900.00, FALSE),  -- 19
    ('Nissan',     'Kicks Advance',        2022, 1, 112900.00, FALSE),  -- 20
    ('Renault',    'Duster Iconic',        2022, 1, 109900.00, FALSE),  -- 21
    ('Volkswagen', 'Gol 1.0',              2020, 1,  45900.00, TRUE),   -- 22
    ('Honda',      'CG 160 Titan',         2023, 2,  19900.00, FALSE),  -- 23
    ('Yamaha',     'Fazer 250',            2022, 2,  23900.00, FALSE),  -- 24
    ('Honda',      'CB 500F',              2022, 2,  39900.00, TRUE),   -- 25
    ('Yamaha',     'MT-03',                2023, 2,  34900.00, FALSE),  -- 26
    ('Honda',      'Biz 125',              2023, 2,  15900.00, FALSE),  -- 27
    ('BMW',        'G 310 R',              2022, 2,  32900.00, TRUE),   -- 28
    ('Honda',      'PCX 160',              2023, 2,  21900.00, FALSE),  -- 29
    ('Kawasaki',   'Ninja 400',            2022, 2,  41900.00, FALSE),  -- 30
    ('Toyota',     'Hilux SRV',            2022, 3, 259900.00, FALSE),  -- 31
    ('Chevrolet',  'S10 LTZ',              2021, 3, 219900.00, TRUE),   -- 32
    ('Ford',       'Ranger XLT',           2022, 3, 239900.00, FALSE),  -- 33
    ('Mitsubishi', 'L200 Triton',          2021, 3, 199900.00, FALSE),  -- 34
    ('Volkswagen', 'Amarok Highline',      2022, 3, 269900.00, TRUE),   -- 35
    ('Fiat',       'Toro Volcano',         2023, 3, 169900.00, FALSE),  -- 36
    ('Fiat',       'Strada Volcano',       2023, 3, 114900.00, FALSE),  -- 37
    ('Nissan',     'Frontier XE',          2022, 3, 229900.00, FALSE),  -- 38
    ('Ram',        'Rampage Laramie',      2024, 3, 289900.00, FALSE),  -- 39
    ('Toyota',     'Hilux SR',             2020, 3, 189900.00, TRUE),   -- 40
    ('Honda',      'HR-V EXL',             2024, 1, 159900.00, FALSE),  -- 41
    ('Yamaha',     'XJ6 N',                2019, 2,  36900.00, TRUE),   -- 42
    ('Chevrolet',  'Montana Premier',      2024, 3, 139900.00, FALSE),  -- 43
    ('Fiat',       'Pulse Impetus',        2023, 1, 109900.00, FALSE);  -- 44

-- ============================================================
-- VENDAS  (valor_venda = valor negociado, normalmente abaixo do preço anunciado)
-- ============================================================
INSERT INTO carros_vendas (idvendedores, id_carro, data_venda, valor_venda) VALUES
    (1,  1, '2025-12-05', 127500.00),
    (2, 23, '2025-12-12',  19500.00),
    (3,  4, '2025-12-20',  75000.00),
    (1, 31, '2026-01-09', 255000.00),
    (4, 19, '2026-01-22',  47900.00),
    (2,  6, '2026-02-03',  71500.00),
    (5, 27, '2026-02-17',  15500.00),
    (3, 33, '2026-02-26', 234000.00),
    (1, 13, '2026-03-08', 137000.00),
    (6, 24, '2026-03-15',  23000.00),
    (2, 10, '2026-03-28',  81000.00),
    (4, 36, '2026-04-06', 166500.00),
    (1,  3, '2026-04-19',  97000.00),
    (3, 26, '2026-04-30',  34000.00),
    (5, 12, '2026-05-10',  51900.00),
    (2, 32, '2026-05-21', 214000.00),
    (6,  7, '2026-06-04',  93000.00),
    (1, 15, '2026-06-18', 162000.00),
    (3, 29, '2026-06-27',  21500.00),
    (4, 37, '2026-07-09', 112900.00),
    (2, 14, '2026-07-23', 122000.00),
    (1, 39, '2026-08-05', 285000.00),
    (5, 30, '2026-08-19',  40900.00),
    (3,  9, '2026-09-02', 102500.00),
    (6, 34, '2026-09-16', 196000.00),
    (2,  2, '2026-09-29', 117500.00),
    (1, 18, '2026-10-07', 140000.00),
    (4, 25, '2026-10-21',  39000.00),
    (3, 11, '2026-10-30', 115900.00),
    (2, 38, '2026-11-06', 226000.00),
    (1, 20, '2026-11-14', 110500.00),
    (7,  5, '2026-11-18',  63900.00);

-- numero_vendas de cada vendedor = quantidade de vendas dele (SUBQUERY correlacionada)
UPDATE vendedores v
SET numero_vendas = (SELECT COUNT(*) FROM carros_vendas cv WHERE cv.idvendedores = v.id);
