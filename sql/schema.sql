-- Rodar no banco loja_carros (Query Tool do pgAdmin)

DROP TABLE IF EXISTS carros_vendas;
DROP TABLE IF EXISTS estoque;
DROP TABLE IF EXISTS vendedores;

CREATE TABLE vendedores (
    id            SERIAL PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL,
    numero_vendas INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE estoque (
    id_carro     SERIAL PRIMARY KEY,
    tipo_veiculo INTEGER NOT NULL,
    consignado   BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE carros_vendas (
    token_venda  SERIAL PRIMARY KEY,
    idvendedores INTEGER NOT NULL REFERENCES vendedores (id),
    id_carro     INTEGER NOT NULL REFERENCES estoque (id_carro)
);
