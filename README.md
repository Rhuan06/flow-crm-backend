# 🚀 FlowCRM — Backend API

<p align="center">
  **Uma API RESTful para gerenciamento inteligente de clientes e oportunidades de vendas.**
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
| Uvicorn | Servidor ASGI |

## ✨ Funcionalidades

### 🔐 Autenticação e segurança
- Autenticação utilizando JWT (JSON Web Token).
- Proteção de endpoints por autenticação.
- Controle de usuários e permissões.
- Gerenciamento de usuários ativos.

### 👥 Gestão de clientes
- Cadastro de clientes.
- Listagem de clientes.
- Consulta individual.
- Atualização de informações.
- Exclusão de registros.
- Associação dos clientes ao usuário responsável.

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
- Prevenção de valores negativos.
- Validação de campos obrigatórios.
- Isolamento de dados por `owner_id`.
- Verificação de propriedade dos registros antes das operações.

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