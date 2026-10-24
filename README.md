# Crudzinho — Loja de Carros

Sistema CRUD de uma loja de veículos, feito em Django com PostgreSQL.

Depois de fazer login, o usuário pode:

- **Vendedores:** cadastrar, listar, editar e excluir, com busca por nome.
- **Estoque:** cadastrar, listar, editar e excluir veículos, com filtro por tipo e por consignado.
- **Vendas:** registrar uma venda ligando um vendedor a um veículo do estoque, com filtro por vendedor e por tipo de veículo.

As páginas só abrem com login. Não é possível excluir um vendedor ou um veículo que já tem venda registrada, por causa da chave estrangeira.

## Tecnologias

- Python 3.13
- Django 5.2
- PostgreSQL 17
- psycopg 3 (driver do PostgreSQL)

## Banco de dados

| Tabela          | Colunas                                                    |
|-----------------|------------------------------------------------------------|
| `vendedores`    | `id` (PK), `nome`, `numero_vendas`                         |
| `estoque`       | `id_carro` (PK), `tipo_veiculo`, `consignado`              |
| `carros_vendas` | `token_venda` (PK), `idvendedores` (FK), `id_carro` (FK)   |

Relacionamentos:

- `carros_vendas.idvendedores` → `vendedores.id`
- `carros_vendas.id_carro` → `estoque.id_carro`

Um vendedor pode ter várias vendas, e um veículo pode aparecer em várias vendas.

`tipo_veiculo`: 1 = Carro, 2 = Moto, 3 = Caminhonete.

### Arquivos SQL

- [`sql/schema.sql`](sql/schema.sql): criação das tabelas.
- [`sql/consultas.sql`](sql/consultas.sql): os comandos que o sistema executa, com `INSERT`, `SELECT` com filtros, `UPDATE`, `DELETE`, os `JOIN` das vendas e consultas de relatório.

## Configuração do banco de dados

1. No PostgreSQL (pgAdmin ou psql), crie o banco:

   ```sql
   CREATE DATABASE loja_carros;
   ```

2. Conectado ao banco `loja_carros`, rode o conteúdo de `sql/schema.sql` para criar as tabelas.

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

Acesse http://127.0.0.1:8000.

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
│   ├── views.py           # telas do CRUD e filtros
│   ├── urls.py            # rotas
│   └── templates/core/    # páginas HTML
├── templates/registration/login.html
└── sql/
    ├── schema.sql
    └── consultas.sql
```
