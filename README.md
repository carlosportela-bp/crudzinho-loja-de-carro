# Crudzinho — Loja de Carros

Sistema de informação de uma loja de veículos, feito em Django com PostgreSQL.
Além do CRUD de vendedores, estoque e vendas, tem um **Dashboard** com indicadores (KPIs)
e gráficos alimentados por consultas SQL reais ao banco.

## Aluno

- **Nome:** Cadu Portela
- **GitHub:** [carlosportela-bp](https://github.com/carlosportela-bp)

## Funcionalidades

Depois de fazer login, o usuário pode:

- **Dashboard:** KPIs, gráficos e tabelas de análise das vendas e do estoque.
- **Vendedores:** cadastrar, listar, editar e excluir, com busca por nome.
- **Estoque:** cadastrar, listar, editar e excluir veículos (marca, modelo, ano, tipo, preço, consignado), com filtro por tipo e por consignado.
- **Vendas:** registrar uma venda ligando um vendedor a um veículo do estoque, com data e valor negociado, e filtrar por vendedor e por tipo de veículo.

As páginas só abrem com login. Não é possível excluir um vendedor ou um veículo que já tem venda registrada, por causa da chave estrangeira.

## Dashboard

Acesse em http://127.0.0.1:8000/dashboard/. Cada cartão mostra quais recursos SQL usa e tem um botão **Ver SQL** com a consulta executada.

**Indicadores (KPIs)**

| KPI                   | O que mostra                                                         | SQL                     |
|-----------------------|----------------------------------------------------------------------|-------------------------|
| Faturamento total     | Soma de todas as vendas e quantidade de veículos vendidos            | `SUM`, `COUNT`          |
| Ticket médio          | Valor médio de cada venda                                            | `AVG`                   |
| Maior venda           | Venda de maior valor, com o veículo e o vendedor                     | `MAX`, `SUBQUERY`, `JOIN` |
| Menor venda           | Venda de menor valor, com o veículo e o vendedor                     | `MIN`, `SUBQUERY`, `JOIN` |
| Veículos disponíveis  | Veículos ainda não vendidos, valor parado em estoque e faixa de preço | `MIN`, `MAX`, `SUBQUERY` |
| Vendedor destaque     | Vendedor que mais faturou                                            | `JOIN`, `GROUP BY`      |

**Gráficos** (Chart.js)

| Gráfico                         | Tipo               | SQL                              |
|---------------------------------|--------------------|----------------------------------|
| Faturamento por mês             | Linhas             | `GROUP BY`                       |
| Faturamento por vendedor        | Barras             | `LEFT JOIN`, `GROUP BY`          |
| Vendas por tipo de veículo      | Rosca              | `JOIN`, `GROUP BY`               |
| Marcas com 2 ou mais vendas     | Barras horizontais | `JOIN`, `GROUP BY`, `HAVING`     |

**Tabelas**

| Tabela                         | O que mostra                                                     | SQL                                                 |
|--------------------------------|------------------------------------------------------------------|-----------------------------------------------------|
| Vendedores acima da média      | Quem faturou mais que a média por vendedor, com menor e maior venda | `JOIN`, `GROUP BY`, `HAVING`, `SUBQUERY`, `MIN`, `MAX` |
| Estoque disponível por tipo    | Quantidade, preço mínimo, máximo e médio dos veículos não vendidos | `MIN`, `MAX`, `GROUP BY`, `SUBQUERY`               |

As consultas ficam em [`core/dashboard.py`](core/dashboard.py) (executadas com `connection.cursor()`) e o mesmo texto está em [`sql/dashboard.sql`](sql/dashboard.sql), para rodar no pgAdmin.

## Tecnologias

- Python 3.13
- Django 5.2
- PostgreSQL 17
- psycopg 3 (driver do PostgreSQL)
- Chart.js 4 (gráficos, carregado por CDN)

## Banco de dados

| Tabela          | Colunas                                                                               |
|-----------------|---------------------------------------------------------------------------------------|
| `vendedores`    | `id` (PK), `nome`, `numero_vendas`                                                    |
| `estoque`       | `id_carro` (PK), `marca`, `modelo`, `ano`, `tipo_veiculo`, `preco`, `consignado`      |
| `carros_vendas` | `token_venda` (PK), `idvendedores` (FK), `id_carro` (FK), `data_venda`, `valor_venda` |

Relacionamentos:

- `carros_vendas.idvendedores` → `vendedores.id`
- `carros_vendas.id_carro` → `estoque.id_carro`

Um vendedor pode ter várias vendas. `tipo_veiculo`: 1 = Carro, 2 = Moto, 3 = Caminhonete.
`preco` é o preço anunciado do veículo e `valor_venda` é o valor negociado na venda.

### Arquivos SQL

- [`sql/schema.sql`](sql/schema.sql): criação das tabelas.
- [`sql/dados.sql`](sql/dados.sql): dados de exemplo (8 vendedores, 44 veículos e 32 vendas de dez/2025 a nov/2026).
- [`sql/dashboard.sql`](sql/dashboard.sql): consultas dos KPIs, gráficos e tabelas do dashboard.
- [`sql/consultas.sql`](sql/consultas.sql): comandos do CRUD (`INSERT`, `SELECT` com filtros, `UPDATE`, `DELETE`, `JOIN`).

## Configuração do banco de dados

1. No PostgreSQL (pgAdmin ou psql), crie o banco:

   ```sql
   CREATE DATABASE loja_carros;
   ```

2. Conectado ao banco `loja_carros`, rode `sql/schema.sql` (cria as tabelas) e depois `sql/dados.sql` (insere os dados de exemplo). Pelo psql:

   ```bash
   psql -U postgres -d loja_carros -f sql/schema.sql -f sql/dados.sql
   ```

   O `schema.sql` apaga e recria as tabelas, então rodá-lo de novo zera os dados.

3. O projeto se conecta, por padrão, com:

   | Configuração | Valor         |
   |--------------|---------------|
   | Banco        | `loja_carros` |
   | Usuário      | `postgres`    |
   | Senha        | `root`        |
   | Host         | `localhost`   |
   | Porta        | `5432`        |

   Para usar outros valores, defina as variáveis de ambiente `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT`.

## Como executar

```bash
git clone https://github.com/carlosportela-bp/crudzinho-loja-de-carro.git
cd crudzinho-loja-de-carro

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

O `migrate` cria só as tabelas internas do Django (login e sessões). As tabelas do sistema vêm do `sql/schema.sql`.

Acesse http://127.0.0.1:8000 e, depois do login, abra o **Dashboard**.

## Usuário para teste

Crie o usuário com `python manage.py createsuperuser` usando:

- **Usuário:** `admin`
- **Senha:** `admin123`

Se o Django avisar que a senha é muito comum, responda `y` para confirmar.

## Estrutura de pastas

```
crudzinho-loja-de-carro/
├── manage.py
├── requirements.txt
├── loja/                  # configurações do projeto (settings, urls)
├── core/                  # app principal
│   ├── models.py          # Vendedor, Estoque, CarroVenda
│   ├── forms.py           # formulários do CRUD
│   ├── views.py           # telas do CRUD, filtros e dashboard
│   ├── dashboard.py       # consultas SQL do dashboard
│   ├── urls.py            # rotas
│   └── templates/core/    # páginas HTML (dashboard.html e telas do CRUD)
├── templates/registration/login.html
└── sql/
    ├── schema.sql
    ├── dados.sql
    ├── dashboard.sql
    └── consultas.sql
```
