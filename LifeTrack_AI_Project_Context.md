# LifeTrack AI --- Project Context & Handoff

> **Purpose:** This file is the portable source of truth for the
> LifeTrack AI project. It is written so it can be shared with another
> AI assistant, opened on another device, or used as project
> documentation without relying on previous chat history.
>
> **Last updated:** 24 November 2026\
> **Project type:** Personal learning + portfolio project\
> **Primary focus:** Python Backend Engineering + Applied Generative AI

------------------------------------------------------------------------

## 1. Project at a glance

**LifeTrack AI** is a multi-user, AI-powered personal life-management
platform. It is intended to help a person organize important information
and everyday responsibilities in one place, then use an AI assistant to
understand that information and help with useful tasks.

The project combines a conventional backend application with practical
GenAI capabilities. It is not intended to be just a chatbot. The AI
should work with information and features that already exist in the
application, using controlled tools and permission checks.

### Core idea

A user should be able to:

-   Store and organize personal documents and important information.
-   Track bills, due dates, tasks, and reminders.
-   Keep useful health-related records and appointment information
    organized.
-   View relevant information through a central dashboard.
-   Ask a central AI assistant questions about their own stored
    information.
-   Get summaries, extracted details, and suggestions based on their
    data.
-   Trigger supported actions through the assistant, with confirmation
    before consequential actions.

### Example user scenarios

1.  A user uploads a bill. The system stores its details and can help
    identify the amount and due date.
2.  A user asks, "Which bills are due this week?" The assistant
    retrieves the user's relevant records and summarizes them.
3.  A user stores an appointment. The system can show it on the
    dashboard and support a reminder workflow.
4.  A user uploads a document and asks a question about it. The
    assistant retrieves relevant document content and answers with
    context.
5.  A user asks for a summary of their stored records. The assistant
    uses authorized application tools rather than inventing information.

These are product goals. Do not claim that all these features have
already been implemented.

------------------------------------------------------------------------

## 2. Project goals

### Engineering goals

-   Build a maintainable backend using **Python and FastAPI**.
-   Use PostgreSQL for persistent relational data.
-   Use SQLAlchemy for database access and Alembic for schema
    migrations.
-   Implement authentication, validation, and authorization properly.
-   Build real application features instead of unrelated toy exercises.
-   Integrate GenAI in a way that is grounded in user data.
-   Learn production-oriented backend patterns while building the
    application.
-   Keep the project modular and testable.

### Learning and portfolio goals

The project is also a hands-on learning path for:

-   Python backend development.
-   REST API design.
-   FastAPI dependency injection and middleware.
-   SQL, PostgreSQL, SQLAlchemy, and database migrations.
-   Authentication, JWT, password hashing, and authorization.
-   Testing, Docker, and CI/CD fundamentals.
-   LLM integration, prompt design, embeddings, vector search, and RAG.
-   LangChain and LangGraph.
-   Agent tools, controlled workflows, and human approval for sensitive
    actions.

The project is independent portfolio work. Do not describe it as work
completed for an employer.

------------------------------------------------------------------------

## 3. Technology stack

### Current foundation

  -----------------------------------------------------------------------
  Area                    Technology              Status / notes
  ----------------------- ----------------------- -----------------------
  Language                Python 3.12.10          Installed

  Backend framework       FastAPI                 Main framework; Django
                                                  is not part of the
                                                  chosen stack

  ASGI server             Uvicorn                 Installed

  Validation / settings   Pydantic, Pydantic      Used for
                          Settings                request/response
                                                  schemas and
                                                  configuration

  Database                PostgreSQL 18           Local database is
                                                  running

  ORM                     SQLAlchemy              Used for database
                                                  models and sessions

  Migrations              Alembic                 Initial users-table
                                                  migration applied

  PostgreSQL driver       Psycopg                 Installed

  Password hashing        `pwdlib[argon2]`        Planned / installation
                                                  and implementation must
                                                  be verified before
                                                  assuming complete

  Frontend                React (planned)         Deferred until backend
                                                  foundation is ready
  -----------------------------------------------------------------------

### Planned GenAI and infrastructure components

These are roadmap choices, not necessarily implemented yet.

  -----------------------------------------------------------------------
  Area                    Candidate technology    Intended use
  ----------------------- ----------------------- -----------------------
  LLM integration         Gemini API or a         Natural-language
                          lightweight local model understanding and
                                                  generation

  LLM framework           LangChain               Model, prompt,
                                                  retrieval, and tool
                                                  integration

  Agent workflow          LangGraph               Controlled multi-step
                                                  assistant workflows

  Embeddings              Embedding model         Convert document chunks
                          selected after resource into vectors
                          testing                 

  Vector search           pgvector with           Similarity search over
                          PostgreSQL              user-authorized content

  Retrieval               RAG                     Ground answers in
                                                  relevant stored
                                                  documents

  Background jobs         Celery and Redis, if    Reminders, document
                          needed                  processing, and
                                                  longer-running tasks

  Containerization        Docker                  Reproducible local and
                                                  deployment environment

  Testing                 pytest                  Unit and
                                                  API/integration tests

  CI                      GitHub Actions          Automated checks and
                                                  tests

  Cloud                   Not selected for now    Avoid unnecessary cloud
                                                  spend during learning
  -----------------------------------------------------------------------

**Hardware constraint:** Development is on a Windows PC with an Intel i7
8th-generation CPU, 16 GB RAM, and approximately 20--30 GB free disk
space. Prefer free or low-cost services and lightweight local models. Do
not recommend large models or expensive cloud infrastructure without
explaining the resource and cost impact.

------------------------------------------------------------------------

## 4. Current development environment

Known local environment:

-   Operating system: Windows.
-   Shell: PowerShell.
-   Editor: VS Code.
-   Python: `3.12.10`.
-   pip: `25.0.1`.
-   FastAPI: `0.162.5`.
-   Uvicorn: `0.54.0`.
-   PostgreSQL: `18`.
-   PostgreSQL Windows service: `postgresql-x64-18`.
-   Database name: `lifetrack_ai`.
-   Application database user: `lifetrack_user`.

Local project directory:

``` text
C:\Users\Rajesh\OneDrive\Desktop\Folder\lifetrack_ai
```

Do not ask the user to paste or expose the real `.env` file or database
password. Use `.env.example` when sharing configuration.

------------------------------------------------------------------------

## 5. Current folder structure

The following is the known structure at the latest project checkpoint.
Some folders are placeholders for future modules.

``` text
lifetrack_ai/
│
├── alembic/
│   ├── versions/
│   │   └── 43f5b4c3d765_create_users_table.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── health.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   └── health.py
│   │
│   ├── services/
│   │   └── __init__.py
│   │
│   └── main.py
│
├── venv/
├── requirements.txt
├── .env
├── .env.example
└── .gitignore
```

### What each area is for

  -----------------------------------------------------------------------
  Path                                Responsibility
  ----------------------------------- -----------------------------------
  `app/main.py`                       Creates the FastAPI application and
                                      registers top-level routers

  `app/api/v1/router.py`              Combines API endpoint routers under
                                      version 1

  `app/api/v1/endpoints/`             Contains route handlers grouped by
                                      feature

  `app/core/`                         Application configuration and
                                      cross-cutting security utilities

  `app/database/`                     SQLAlchemy base, engine, session
                                      factory, and DB dependency

  `app/models/`                       SQLAlchemy database table models

  `app/schemas/`                      Pydantic request and response
                                      schemas

  `app/services/`                     Business logic, kept separate from
                                      route handlers

  `alembic/`                          Database migration configuration
                                      and revision files

  `.env`                              Local secrets and
                                      environment-specific configuration;
                                      never commit

  `.env.example`                      Safe template showing required
                                      environment variable names

  `requirements.txt`                  Python dependencies

  `.gitignore`                        Excludes virtual environments,
                                      secrets, caches, and generated
                                      files
  -----------------------------------------------------------------------

As the application grows, add feature modules deliberately. A possible
future organization is:

``` text
app/
├── api/
│   └── v1/
│       ├── router.py
│       └── endpoints/
│           ├── auth.py
│           ├── users.py
│           ├── documents.py
│           ├── bills.py
│           ├── tasks.py
│           ├── reminders.py
│           └── assistant.py
│
├── core/
│   ├── config.py
│   └── security.py
│
├── database/
│   ├── base.py
│   └── session.py
│
├── models/
│   ├── user.py
│   ├── document.py
│   ├── bill.py
│   ├── task.py
│   └── reminder.py
│
├── schemas/
│   ├── user.py
│   ├── document.py
│   ├── bill.py
│   ├── task.py
│   └── reminder.py
│
├── services/
│   ├── auth_service.py
│   ├── document_service.py
│   ├── reminder_service.py
│   └── assistant_service.py
│
└── main.py
```

This second tree is a suggested future structure, not a claim about
files that already exist. Do not create all these files at once. Add
them when implementing the corresponding features.

------------------------------------------------------------------------

## 6. Current implementation status

### 6.1 FastAPI application

The application is created in `app/main.py`. It:

-   Creates a `FastAPI` instance.
-   Uses settings from `app/core/config.py`.
-   Sets the application title, description, version, and debug mode.
-   Registers the API v1 router using the configured API prefix.
-   Exposes a simple root endpoint.

Known implementation:

``` python
from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered personal information and management platform",
    version="1.0.0",
    debug=settings.DEBUG,
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} backend is running"}
```

### 6.2 API router

`app/api/v1/router.py` creates an `APIRouter` and includes the health
endpoint router. The application-level prefix is configured in
`main.py`.

The health route is therefore available at:

``` text
GET /api/v1/health
```

assuming `API_V1_PREFIX=/api/v1`.

### 6.3 Configuration

`app/core/config.py` loads application configuration through Pydantic
Settings. Values are supplied through environment variables and `.env`.

Known configuration concepts include:

-   `APP_NAME`
-   `APP_ENV`
-   `DEBUG`
-   `API_V1_PREFIX`
-   `DB_HOST`
-   `DB_PORT`
-   `DB_NAME`
-   `DB_USER`
-   `DB_PASSWORD`

Never put real secrets in source code or commit `.env`.

### 6.4 Database connection and dependency

`app/database/session.py` creates the SQLAlchemy engine and session
factory. It also provides a `get_db()` generator dependency.

The essential pattern is:

``` python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Meaning:

1.  A database session is created for the request.
2.  `yield` provides that session to the endpoint.
3.  The endpoint uses the session.
4.  FastAPI runs the dependency cleanup after the request.
5.  `db.close()` releases the session's resources.

Closing a session is not the same as committing a transaction. Use
`commit()` to persist a transaction; use `rollback()` when an
uncommitted transaction must be reversed.

### 6.5 Database base and model registration

`app/database/base.py` defines the SQLAlchemy declarative base and
imports the user model so it is registered in `Base.metadata` for
Alembic.

### 6.6 User model and database

A `users` table has been created in PostgreSQL through Alembic.

Known columns:

  -----------------------------------------------------------------------
  Column                  Type                    Constraints / behavior
  ----------------------- ----------------------- -----------------------
  `id`                    integer                 Primary key, generated
                                                  sequence

  `email`                 varchar(255)            Not null, unique index

  `full_name`             varchar(100)            Not null

  `password_hash`         varchar(255)            Not null

  `is_active`             boolean                 Not null

  `created_at`            timestamptz             Not null, default
                                                  `now()`

  `updated_at`            timestamptz             Not null, default
                                                  `now()`, updated by ORM
                                                  on update
  -----------------------------------------------------------------------

Database name: `lifetrack_ai`.

The initial Alembic migration was generated and applied successfully.
The PostgreSQL table was inspected using `\d users`.

### 6.7 Health endpoint

`app/api/v1/endpoints/health.py` exposes a health-check endpoint. It
executes:

``` python
db.execute(text("SELECT 1"))
```

This checks whether the application can execute a simple query against
the database. It does not require any application table.

The response schema is defined in `app/schemas/health.py`.

A successful response was observed:

``` json
{
  "status": "healthy",
  "application": "LifeTrack AI",
  "version": "1.0.0"
}
```

This confirms that the FastAPI health route and database connectivity
were working at that checkpoint. Re-test locally before assuming the
environment is still running.

------------------------------------------------------------------------

## 7. Backend concepts already covered

These concepts have been discussed while building the project. The next
AI assistant should build on them instead of restarting from zero.

### Models vs schemas

-   **SQLAlchemy model:** describes how data is stored in a database
    table.
-   **Pydantic schema:** describes and validates the data accepted by an
    API or returned by an API.
-   A request schema and response schema can be different.
-   Use `response_model` to control and validate the response shape
    returned by an endpoint.

### FastAPI dependency injection

Example:

``` python
def read_items(db: Session = Depends(get_db)):
    ...
```

-   `Depends(get_db)` tells FastAPI that the endpoint needs the result
    of `get_db`.
-   FastAPI calls the dependency and injects the yielded database
    session into `db`.
-   This avoids manually creating and closing a database session in
    every endpoint.

### SQLAlchemy session and transactions

-   `db.add(object)` stages an object in the session; it does not by
    itself guarantee a committed database record.
-   `db.flush()` sends pending SQL statements to the database within the
    current transaction, but does not commit.
-   `db.commit()` commits the transaction.
-   `db.rollback()` reverses uncommitted transaction changes.
-   `db.close()` closes/releases the session resources.

### Password hashing

The intended approach is to hash passwords with a password-hashing
algorithm such as Argon2. Store only the password hash, never the
original password.

The `pwdlib[argon2]` installation and the `app/core/security.py`
implementation were discussed, but their completion was not confirmed in
the latest checkpoint. Verify before relying on them.

### JWT and FastAPI token handling

A minimal FastAPI integration can use:

-   `OAuth2PasswordBearer` to extract a Bearer token from the
    `Authorization` header.
-   `Depends(...)` to inject that token into a protected route.

Important distinction: `OAuth2PasswordBearer` extracts the token. It
does **not** create a JWT, verify its signature, validate its expiry, or
authenticate the user by itself. A separate dependency/service must
validate the token using the chosen JWT library.

### CORS

FastAPI supports CORS through `CORSMiddleware`, provided by Starlette:

``` python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

-   `allow_origins` lists frontend origins allowed to access the backend
    from a browser.
-   `allow_methods` controls permitted HTTP methods.
-   `allow_headers` controls permitted request headers.
-   `allow_credentials` controls whether browser credentials such as
    cookies can be included.
-   In production, specify the real frontend domain. Do not combine
    credentialed requests with a wildcard origin.
-   CORS is a browser-enforced cross-origin policy; it is not a
    replacement for authentication or authorization.

------------------------------------------------------------------------

## 8. Product architecture direction

The intended architecture is a **modular monolith first**, not a
microservices system.

A simplified future request flow:

``` text
React Frontend
      |
      | HTTPS / REST API
      v
FastAPI Application
      |
      +---- Authentication / Authorization
      |
      +---- API endpoints
      |        |
      |        +---- User and profile services
      |        +---- Document services
      |        +---- Bills / tasks / reminder services
      |        +---- AI assistant endpoint
      |
      +---- PostgreSQL
      |        |
      |        +---- Application records
      |        +---- Document metadata
      |        +---- Vector embeddings (planned with pgvector)
      |
      +---- Background worker (planned if needed)
      |        |
      |        +---- Reminders
      |        +---- Document processing
      |
      +---- LLM / retrieval / agent workflow (planned)
```

### AI assistant design principles

-   The assistant should answer using the current user's authorized
    data.
-   Retrieve relevant records before answering questions about stored
    information.
-   Use RAG for document-grounded answers.
-   Use application services/tools for actions; do not let the LLM
    directly bypass business rules or database authorization.
-   Validate tool inputs and outputs.
-   Enforce user ownership and permissions at the backend layer.
-   Require explicit user confirmation for consequential actions, such
    as sending, deleting, or changing important records.
-   Keep a clear distinction between model-generated suggestions and
    verified application data.
-   Handle missing information honestly. The assistant must not invent
    bill amounts, dates, appointments, or document contents.

### Multi-user data isolation

The application is intended to support multiple users. Every user-owned
record must be associated with an owner/user ID, and every read, update,
or delete operation must enforce ownership on the backend. Never rely
only on frontend filtering to protect user data.

------------------------------------------------------------------------

## 9. Planned feature areas

These are roadmap areas. Their implementation status must be checked in
the actual repository.

### A. Authentication and users

-   User registration.
-   Email validation/verification if included in the chosen scope.
-   Password hashing.
-   Login.
-   JWT access-token generation and validation.
-   Protected routes.
-   User profile.
-   Role/permission handling only where the product requires it.

### B. Documents

-   Upload and store document files safely.
-   Store metadata in PostgreSQL.
-   Associate each document with its owner.
-   Extract text from supported document types.
-   Track processing status and extraction errors.
-   Chunk extracted text for retrieval.
-   Generate embeddings and store them for similarity search.
-   Enforce document ownership during retrieval.

### C. Bills and reminders

-   Store bill details and due dates.
-   Track status and payment-related metadata where appropriate.
-   Create reminder records.
-   Support scheduled reminder delivery through a background worker if
    required.
-   Avoid claiming that a bill was paid or a reminder was sent unless
    the system confirms it.

### D. Tasks and appointments

-   Create, update, complete, and list tasks.
-   Store appointment details.
-   Support due dates and reminder preferences.
-   Display relevant information in the dashboard.

### E. AI assistant and RAG

-   Accept a user's question.
-   Identify whether it requires general knowledge or the user's own
    data.
-   Retrieve relevant authorized records for personal-data questions.
-   Generate an answer grounded in retrieved content.
-   Return useful source references where feasible.
-   Handle no-result cases instead of hallucinating.
-   Add LangGraph workflows when the assistant needs controlled
    multi-step reasoning or tool execution.

### F. Dashboard and frontend

-   React frontend is planned but deferred.
-   Dashboard should show useful summaries from real backend records.
-   Frontend should use authenticated API calls.
-   Backend CORS configuration should allow only the intended frontend
    origins.

------------------------------------------------------------------------

## 10. Suggested implementation order

Build one vertical slice at a time. Do not create every planned module
before the previous feature works.

1.  Finish authentication foundations: password hashing, registration,
    login, token creation, token validation, and protected route.
2.  Add user profile and enforce user ownership.
3.  Add one real document-upload workflow.
4.  Extract and store document text and metadata.
5.  Add document retrieval and RAG.
6.  Add the first useful AI assistant endpoint grounded in the user's
    documents.
7.  Add bills/tasks and reminders based on the actual MVP priorities.
8.  Add background processing only when a real workflow needs it.
9.  Add automated tests for security, ownership, API behavior, and
    failure cases.
10. Add Docker and CI checks.
11. Build the React frontend after the backend contracts are stable.
12. Add LangGraph and additional tools only when they solve a concrete
    workflow.

This order is a suggested roadmap, not a statement that the work is
already done.

------------------------------------------------------------------------

## 11. Development and teaching rules for an AI assistant

When helping with this project, follow these instructions.

### Teaching style

-   Teach in simple English, from fundamentals.
-   Explain what a concept means, why it is needed, and how it works in
    this project.
-   Move one step at a time. Do not dump an entire feature or roadmap
    into one lesson.
-   Do not move to the next step until the user says to continue or asks
    the next question.
-   Use practical project examples instead of unrelated toy examples
    wherever possible.
-   Do not assume the user already understands a term just because it is
    common in backend development.
-   Be direct. Correct misunderstandings clearly.
-   Keep explanations concise and avoid unnecessary theory.

### Code instructions

-   Explain **every line of code** with a short explanation, preferably
    as a concise inline comment or immediately adjacent explanation.
-   When changing a project file, state the exact file path.
-   When asked to provide a replacement file, provide the complete
    copy-paste-ready file, not a partial fragment.
-   Explain briefly what changed and why.
-   Do not add docstrings unless requested.
-   Do not silently change file names, folder structure, libraries, or
    architecture.
-   Do not invent files, functions, endpoints, database columns, or
    implementation details.
-   Before suggesting commands that change the environment, explain what
    they do.
-   Use PowerShell commands for this Windows development environment.
-   Never ask the user to share passwords, API keys, tokens, or the
    contents of `.env`.

### Project discipline

-   Prefer real, useful application features over dummy data and
    throwaway exercises.
-   Keep the design understandable and maintainable.
-   Do not over-engineer with microservices or complex infrastructure.
-   Prefer free/local options where practical.
-   Explain any paid API, cloud resource, or hardware requirement before
    recommending it.
-   Do not claim a feature is complete until it has been implemented and
    verified.
-   Distinguish clearly between **implemented**, **in progress**,
    **planned**, and **not decided**.
-   If the actual repository differs from this document, trust the
    current repository and ask for the relevant file or command output
    before making assumptions.

------------------------------------------------------------------------

## 12. How to run the project

From the project root in PowerShell:

``` powershell
# Activate the existing virtual environment.
.\venv\Scripts\Activate.ps1

# Start the FastAPI development server with automatic reload.
python -m uvicorn app.main:app --reload
```

Expected local URLs, assuming the default port and API prefix:

-   Root: `http://127.0.0.1:8000/`
-   Health check: `http://127.0.0.1:8000/api/v1/health`
-   Swagger UI: `http://127.0.0.1:8000/docs`
-   ReDoc: `http://127.0.0.1:8000/redoc`

If the virtual environment or dependencies are missing on another
device:

``` powershell
# Create a virtual environment using the installed Python.
python -m venv venv

# Activate the virtual environment.
.\venv\Scripts\Activate.ps1

# Install the dependencies recorded by the project.
python -m pip install -r requirements.txt
```

The PostgreSQL server and database must also be configured on the new
device. Copy `.env.example` to `.env` and fill in local values
privately. Never copy real secrets into this handoff file.

------------------------------------------------------------------------

## 13. Git and portability checklist

To use the project on another device:

1.  Push the source code to the intended private or public Git
    repository.
2.  Ensure `.env` and `venv/` are excluded from Git.
3.  Commit `.env.example` with placeholder values only.
4.  Include the current `requirements.txt`.
5.  Install Python and PostgreSQL on the new device.
6.  Create the local database and application database user.
7.  Configure a new local `.env`.
8.  Install dependencies.
9.  Run Alembic migrations.
10. Start Uvicorn and test `/docs` and `/api/v1/health`.

Useful checks before sharing:

``` powershell
# Show the current Git working-tree state.
git status

# Show the installed dependency list.
python -m pip freeze

# Apply all migrations up to the latest revision.
alembic upgrade head

# Show the current migration revision.
alembic current
```

Do not put credentials, private user data, uploaded personal documents,
or production database dumps into the repository.

------------------------------------------------------------------------

## 14. Important known facts vs. unknowns

A future assistant must not fill these gaps with guesses.

### Known at the latest checkpoint

-   The project is called LifeTrack AI.
-   It is a FastAPI backend project using Python 3.12.
-   PostgreSQL 18, SQLAlchemy, Psycopg, and Alembic are in the
    foundation.
-   The initial `users` table migration was applied.
-   The health endpoint successfully queried the database.
-   API version prefix is configured as `/api/v1`.
-   The frontend is deferred.
-   The intended architecture is a modular monolith.
-   GenAI, RAG, embeddings, pgvector, and LangGraph are planned parts of
    the product direction.

### Must be verified in the current repository

-   Whether password hashing dependency `pwdlib[argon2]` is installed.
-   Whether `app/core/security.py` exists and works.
-   Whether registration and login endpoints exist.
-   Whether JWT generation and validation are implemented.
-   Whether tests have been added and pass.
-   Whether any document, bill, task, reminder, or AI endpoint exists.
-   Whether Docker configuration exists.
-   Whether the GitHub repository has the latest local changes.

### Not decided / do not assume

-   Final LLM provider or model.
-   Final embedding model.
-   Whether Redis/Celery are necessary for the MVP.
-   Final frontend implementation details.
-   Production hosting provider.
-   Final billing, notification, or document-storage provider.

------------------------------------------------------------------------

## 15. Prompt to give another AI

Copy the prompt below together with this Markdown file when starting a
new conversation:

> I am building **LifeTrack AI**, a practical portfolio project for
> Python Backend Engineering and Applied GenAI. Read the attached
> project context file fully before suggesting changes.
>
> Treat the file as project history and context, but verify the actual
> repository before assuming a feature is implemented. Clearly
> distinguish implemented features from planned features.
>
> I use Windows, PowerShell, VS Code, Python 3.12, FastAPI, PostgreSQL,
> SQLAlchemy, and Alembic. I want to build the backend step by step,
> then add GenAI capabilities such as RAG and controlled agent
> workflows. Django is not part of the chosen stack.
>
> Teach in simple English, one step at a time. Explain every line of
> code with a short explanation. When editing a file, give its exact
> path and the complete replacement file if a full-file change is
> needed. Do not jump ahead, over-engineer, invent implementation
> details, or use unnecessary dummy data. Wait for me to say "next"
> before moving to the next implementation step.
>
> First, ask me for the current folder tree or the specific file needed
> to verify where the project stands, unless I have already supplied it
> in this conversation.

------------------------------------------------------------------------

## 16. Document maintenance

Update this file whenever an important project decision or
implementation milestone changes.

When updating it:

-   Change the **Last updated** date.
-   Move completed roadmap items into the implemented section only after
    verification.
-   Update the folder tree to match the real repository.
-   Record important library and architecture decisions.
-   Do not store passwords, tokens, API keys, or private personal
    documents here.
-   Keep this document portable and provider-neutral so any AI assistant
    can understand the project.
