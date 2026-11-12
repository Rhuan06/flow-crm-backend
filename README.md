
# 🚀 FlowCRM — Backend API

<p align="center">
  Uma API RESTful para gerenciamento inteligente de clientes e oportunidades de vendas.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white" />
</p>

---

## 📌 Sobre o projeto

O **FlowCRM** é uma API RESTful desenvolvida para um sistema de gerenciamento de relacionamento com clientes (CRM).

O projeto foi construído utilizando Python e FastAPI, priorizando a segurança das informações, a organização da arquitetura e a integridade das regras de negócio.

A aplicação possui arquitetura multi-tenant, garantindo que cada usuário gerencie seus próprios dados de forma independente.

## 🛠️ Tecnologias

| Tecnologia | Finalidade |
|---|---|
| Python 3.10+ | Linguagem de programação |
| FastAPI | Desenvolvimento da API REST |
| SQLAlchemy | ORM e gerenciamento de dados |
| PostgreSQL | Banco de dados relacional |
| Pydantic | Validação e serialização de dados |
| JWT | Autenticação e autorização |
| Passlib + Argon2 | Hash seguro de senhas |
| SlowAPI | Limitação de requisições (Rate Limiting) |
| Uvicorn | Servidor ASGI |

## ✨ Funcionalidades

### 🔐 Autenticação e segurança

- Cadastro público de usuários com perfil `SELLER` definido exclusivamente pelo backend.
- Autenticação utilizando JWT (JSON Web Token).
- Proteção de endpoints por autenticação.
- Consulta dos dados do usuário autenticado.
- Recuperação e redefinição de senha por token JWT temporário.
- Validação de escopo específico (`password_reset`) e expiração de 15 minutos para tokens de redefinição.
- Hash de senhas com Argon2 antes do armazenamento no PostgreSQL.
- Proteção contra enumeração de usuários no fluxo de recuperação de senha.
- Rate Limiting por IP nos endpoints de autenticação.

### 👥 Gestão de clientes

- Cadastro de clientes.
- Listagem de clientes.
- Consulta individual.
- Atualização de informações.
- Exclusão de registros.
- Associação dos clientes ao usuário responsável.

### 🎯 Gestão de leads

- Cadastro e gerenciamento de leads.
- Associação dos registros ao usuário responsável.
- Validação dos dados recebidos pela API.

### 📊 Gestão de oportunidades

- Cadastro e gerenciamento de oportunidades comerciais.
- Associação de oportunidades aos clientes.
- Controle de responsáveis.
- Gerenciamento do funil de vendas.
- Validação das transições de status.
- Bloqueio de alterações indevidas em oportunidades finalizadas (`GANHO` / `PERDIDO`).

### 📈 Dashboard

- Endpoint de resumo de indicadores (`/dashboard/summary`).
- Métricas agregadas por usuário.
- Consulta de informações para acompanhamento comercial.

### 🛡️ Integridade e validação

- Validação de dados com Pydantic.
- Validação de formato de e-mail com `EmailStr`.
- Prevenção de valores negativos.
- Validação de campos obrigatórios.
- Verificação de propriedade dos registros antes das operações.

## 🔒 Arquitetura Multi-Tenant e Segurança

O FlowCRM foi estruturado com isolamento de dados por usuário, autenticação baseada em tokens e controles para proteger operações sensíveis.

### Isolamento de dados (`owner_id`)

As consultas e operações de clientes, leads e oportunidades são vinculadas ao identificador do usuário autenticado (`current_user.id`). Dessa forma, cada usuário acessa e gerencia apenas os próprios registros, evitando acesso cruzado entre contas.

### Autenticação JWT e tokens com escopo

- Tokens JWT assinados são utilizados para autenticar as sessões.
- A recuperação de senha utiliza um token temporário com o escopo `password_reset`.
- O token de redefinição possui validade de 15 minutos.
- A validação do escopo impede que um token de acesso comum seja aceito no fluxo de redefinição de senha.

### Hash seguro de senhas com Argon2

As senhas são processadas com Argon2 antes de serem persistidas no PostgreSQL. O sistema armazena o hash, e não a senha em texto puro.

### Controle de privilégios (RBAC)

O cadastro público não permite que o cliente escolha o próprio nível de acesso. O backend define o perfil inicial como `UserRole.SELLER`, e os schemas de entrada não permitem enviar ou alterar esse privilégio durante o registro.

### Validação e proteção contra enumeração

- Os endereços de e-mail são validados com `EmailStr`.
- O fluxo de recuperação de senha utiliza respostas que não revelam se determinado e-mail possui cadastro no sistema.

### Proteção contra abuso (Rate Limiting)

O SlowAPI aplica limites de requisições por IP nos endpoints sensíveis de autenticação:

| Endpoint | Limite |
|---|---:|
| `POST /api/v1/auth/login` | 5 requisições/minuto |
| `POST /api/v1/auth/register` | 5 requisições/minuto |
| `POST /api/v1/auth/forgot-password` | 3 requisições/minuto |
| `POST /api/v1/auth/reset-password` | 5 requisições/minuto |

## 🔑 Endpoints de autenticação

| Método | Rota | Descrição | Limite |
|---|---|---|---:|
| `POST` | `/api/v1/auth/register` | Cadastro público de novos vendedores | 5/min |
| `POST` | `/api/v1/auth/login` | Autenticação e emissão de JWT | 5/min |
| `GET` | `/api/v1/auth/me` | Retorna o perfil do usuário autenticado | — |
| `POST` | `/api/v1/auth/forgot-password` | Inicia o fluxo de recuperação de senha | 3/min |
| `POST` | `/api/v1/auth/reset-password` | Valida o token temporário e redefine a senha | 5/min |

## 🏗️ Arquitetura do projeto

O backend segue uma estrutura modular, separando responsabilidades entre rotas, modelos, schemas e configurações.

```text
flowcrm-backend/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── clients.py
│   │       ├── leads.py
│   │       ├── opportunities.py
│   │       └── dashboard.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── lead.py
│   │   └── opportunity.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── lead.py
│   │   └── opportunity.py
│   │
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Como executar localmente

### Pré-requisitos

- Python 3.10 ou superior.
- PostgreSQL instalado e configurado.
- Git instalado.

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/flowcrm-backend.git

cd flowcrm-backend
```

### 2. Crie o ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente virtual:

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/flowcrm_db

SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Importante:** Nunca compartilhe suas credenciais ou envie o arquivo `.env` para o GitHub.

### 5. Execute a aplicação

```bash
uvicorn app.main:app --reload
```

## 📚 Documentação da API

Com o servidor em execução, acesse a documentação interativa:

| Documentação | Endereço |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

A documentação permite visualizar os endpoints, consultar os schemas e realizar testes diretamente no navegador.

---

## 👨‍💻 Autor

**Rhuan Silva de Oliveira**

Desenvolvedor em formação | Análise e Desenvolvimento de Sistemas.

<p>
  <a href="https://github.com/SEU-USUARIO">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>

---

<p align="center">
  Desenvolvido com 💻 e ☕ utilizando Python e FastAPI.
</p>
