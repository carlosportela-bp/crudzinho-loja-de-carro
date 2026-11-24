-- Rodar no banco loja_carros (Query Tool do pgAdmin ou psql)
-- Depois deste arquivo, rode o sql/dados.sql para carregar os dados de exemplo.

DROP TABLE IF EXISTS carros_vendas;
DROP TABLE IF EXISTS estoque;
DROP TABLE IF EXISTS vendedores;

CREATE TABLE vendedores (
    id            SERIAL PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL,
    numero_vendas INTEGER NOT NULL DEFAULT 0
);

-- tipo_veiculo: 1 = Carro, 2 = Moto, 3 = Caminhonete
CREATE TABLE estoque (
    id_carro     SERIAL PRIMARY KEY,
    marca        VARCHAR(40)    NOT NULL,
    modelo       VARCHAR(60)    NOT NULL,
    ano          INTEGER        NOT NULL,
    tipo_veiculo INTEGER        NOT NULL,
    preco        NUMERIC(12, 2) NOT NULL,   -- preço anunciado
    consignado   BOOLEAN        NOT NULL DEFAULT FALSE
);

CREATE TABLE carros_vendas (
    token_venda  SERIAL PRIMARY KEY,
    idvendedores INTEGER        NOT NULL REFERENCES vendedores (id),
    id_carro     INTEGER        NOT NULL REFERENCES estoque (id_carro),
    data_venda   DATE           NOT NULL DEFAULT CURRENT_DATE,
    valor_venda  NUMERIC(12, 2) NOT NULL    -- valor negociado na venda
);
