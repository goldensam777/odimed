# Odimed

Odimed is a modern platform combining a **Medical SaaS** and a **Social Network**, designed to streamline the practice of healthcare professionals and facilitate interactions with patients.

## 🚀 Features

- **Medical SaaS**:

  - Manage prescriptions (*ordonnances*).
  - Manage patient profiles and medical records (*antécédents*).
  - Handle medical templates and assets (signatures, stamps/cachets, headers).
- **Social & Networking**: Connect doctors and patients in a secure environment.
- **Secure Architecture**:

  - Strict Role-Based Access Control (RBAC).
  - Sensitive health data (like patient lists) is strictly locked behind doctor-only dependencies (`CurrentMedecinDep`).
- **Robust Storage**:

  - A clean storage abstraction layer for user-generated assets.
  - Organized hierarchically (`medecins/{id}/...`) to prepare for future scalable cloud storage migrations (like AWS S3 or Cloudflare R2).

## 🛠 Technology Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [SQLModel](https://sqlmodel.tiangolo.com/), PostgreSQL.
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, shadcn/ui.
- **Infrastructure**: Docker Compose, Traefik.
- **Document Processing**: `python-docx` for smart token extraction in templates.

## 🚦 Getting Started

### Prerequisites

- Docker & Docker Compose
- `uv` (for local Python package management)

### Local Development (Backend)

1. Ensure your PostgreSQL database is running (via Docker Compose or locally).
2. Install dependencies: `uv sync`
3. Run migrations: `uv run alembic upgrade head`
4. Start the server: `uv run fastapi dev`
5. Run tests: `uv run pytest` (Currently at 100% test coverage!)

### Deployment

Refer to `deployment.md` for production deployment instructions using Docker Compose and Traefik.
