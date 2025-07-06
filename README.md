# NextJS-FastAPI Fullstack Template
This project is a fullstack template combining [Next.js](https://nextjs.org/) for the frontend and [FastAPI](https://fastapi.tiangolo.com/) for the backend. Both components are containerized using Docker for easy deployment and development.

## Features
- **Next.js Frontend**: A React-based framework for building user interfaces
- **FastAPI Backend**: A modern, fast Python web framework for building APIs
- **Database**: PostgreSQL with [SQLAlchemy](https://www.sqlalchemy.org/) ORM, [Alembic](https://alembic.sqlalchemy.org/) for migrations
- **Docker Integration**: Containerized setup for both frontend and backend
- **Testing**: Pytest for backend unit tests
- **Linting & Formatting**: [Ruff](https://github.com/astral-sh/ruff) for Backend and [Prettier](https://prettier.io/) for Frontend
- **Task Automation**: [just](https://github.com/casey/just) command runner for development tasks
- **Environment Configuration**: Simple .env-based configuration (no complex config files)
- **Request/Response Middleware**: Built-in request logging and timing middleware
- **[Optional] Pre-commit Hooks**: [Pre-commit](https://pre-commit.com/) for running linters and formatting checks before commits

## Prerequisites
- **Docker and Docker Compose** installed on your system
- **Python** (^3.13.0) installed on your system
- **Node.js** (^20.0) and npm installed on your system
- **just** command runner installed ([installation guide](https://github.com/casey/just#installation))
  - macOS: `brew install just`
  - Linux: Download from releases or use package manager
  - Windows: `cargo install just` or download from releases

## Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/RockyNiu/nextjs-fastapi.git
   cd nextjs-fastapi
   ```

2. **Set up environment variables:**
   ```bash
   # Copy example environment file
   cp backend/.env.example backend/.env
   # Edit backend/.env with your PostgreSQL credentials
   ```

3. **Start the application:**
   ```bash
   # Start all services with Docker
   just docker-up-all
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

For a complete list of available commands, run `just --list`.

## Development Setup

### Backend Development
The backend uses **PostgreSQL** as the database and **just** for task automation.

#### Environment Setup
1. **Install dependencies:**
   ```bash
   just backend-install
   ```

2. **Set up environment variables:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration
   ```

3. **Database setup:**
   ```bash
   # Start PostgreSQL in Docker
   just docker-up
   
   # Run database migrations
   just db-upgrade
   ```

#### Development Commands
```bash
# Start backend development server
just backend-dev

# Run tests
just backend-test

# Format code
just backend-format

# Lint code
just backend-lint

# Run database migrations
just db-upgrade

# Create new migration
just db-revision "description"
```

#### Debugging in VS Code
1. Start the backend in debug mode:
   ```bash
   just docker-debug
   ```

2. Use the "Backend: debug in docker" launch configuration in VS Code
   - The configuration is pre-configured in `.vscode/launch.json`
   - Set breakpoints in your Python code
   - Press F5 to start debugging

### Frontend Development
1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Frontend Commands:**
   ```bash
   # Format code
   just frontend-format
   
   # Lint code
   just frontend-lint
   
   # Build for production
   just frontend-build
   ```

For more details, see [frontend/README.md](frontend/README.md).

## Project Structure
```text
nextjs-fastapi/
├── backend/
│   ├── alembic/                    # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/
│   │   │   ├── routers/
│   │   │   │   └── item.py
│   │   │   └── middleware.py       # Request/response interceptor
│   │   ├── db/
│   │   │   ├── dao/                # Data Access Objects
│   │   │   │   └── item_dao.py
│   │   │   ├── orm/                # SQLAlchemy models
│   │   │   │   ├── base_orm.py
│   │   │   │   └── item_orm.py
│   │   │   ├── service/            # Business logic layer
│   │   │   │   └── item_service.py
│   │   │   ├── base_dao.py
│   │   │   └── database.py         # Database connection
│   │   ├── entities/               # Domain entities
│   │   │   ├── base.py
│   │   │   └── item.py
│   │   ├── config.py               # Configuration (env-based)
│   │   └── main.py                 # FastAPI application
│   ├── tests/
│   │   ├── db/
│   │   │   └── dao/
│   │   │       └── test_item_dao.py
│   │   ├── utils/
│   │   │   ├── fixtures/
│   │   │   │   └── item_conftest.py
│   │   │   └── utils.py
│   │   └── conftest.py
│   ├── .env                        # Environment variables
│   ├── .env.example               # Example environment file
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── README.md
│   └── ruff.toml
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   │   ├── items/
│   │   │   │   ├── layout.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── favicon.ico
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   └── services/
│   │       ├── apiRequest.ts
│   │       └── itemService.ts
│   ├── Dockerfile
│   ├── next.config.mjs
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── README.md
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── docker/
│   ├── docker-compose.yml
│   ├── docker-compose-frontend.yml
│   └── docker-compose-debug.yml
├── .gitignore
├── justfile                        # Task automation
└── README.md
```
## Configuration

### Environment Variables
The backend uses a simple `.env` file for configuration. Copy `.env.example` to `.env` and adjust the values:

```bash
# Database Configuration (PostgreSQL)
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=template_db

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
APP_ENV=development
```

### Database Setup
The project uses **PostgreSQL** as the primary database:

1. **Using Docker (Recommended):**
   ```bash
   just docker-up  # Starts PostgreSQL in Docker
   ```

2. **Local PostgreSQL:**
   - Install PostgreSQL locally
   - Create a database named `template_db`
   - Update `.env` with your local credentials

3. **Run Migrations:**
   ```bash
   just db-upgrade
   ```

## Command Reference

This project uses [just](https://github.com/casey/just) as a command runner to replace Make. If you don't have `just` installed, see the [installation guide](https://github.com/casey/just#installation).

### Installation
If you don't have `just` installed:

**macOS:**
```bash
brew install just
```

**Other platforms:**
```bash
# Using cargo
cargo install just

# Using npm
npm install -g @antfu/just

# See https://github.com/casey/just#installation for more options
```

### Quick Start
```bash
# Show all available commands
just --list

# Setup development environment
just setup

# Start both frontend and backend development servers
just dev

# Start only backend
just dev-backend

# Start only frontend  
just dev-frontend

# Run database migrations
just migrate

# Run tests
just test
```

### Common Commands

#### Development
- `just dev` - Start both frontend and backend dev servers
- `just dev-backend` - Start FastAPI backend only
- `just dev-frontend` - Start Next.js frontend only
- `just install` - Install all dependencies

#### Database
- `just migrate` - Run database migrations
- `just migration "message"` - Create new migration
- `just db-reset` - Reset database (down and up)
- `just db-history` - Show migration history
- `just db-current` - Show current revision

#### Testing
- `just test` - Run all tests
- `just test-backend` - Run backend tests only
- `just test-frontend` - Run frontend tests only
- `just test-coverage` - Run backend tests with coverage

#### Code Quality
- `just format` - Format all code
- `just lint` - Lint all code
- `just fix` - Fix linting issues automatically

#### Docker
- `just docker-up` - Start all services with Docker
- `just docker-down` - Stop all Docker services
- `just docker-build` - Build Docker images
- `just docker-logs` - View Docker logs

#### Utilities
- `just clean` - Clean up temporary files and caches
- `just status` - Show project status
- `just update` - Update all dependencies
- `just security` - Check for security vulnerabilities

### VS Code Integration

The VS Code tasks have been updated to use `just`:
- Press `Cmd+Shift+P` → "Tasks: Run Task" to see all available tasks
- Press `Cmd+Shift+P` → "Tasks: Run Build Task" to run the default dev servers

### Daily Development Workflow

```bash
# Setup new development environment
just setup

# Daily development workflow
just dev                    # Start both servers
just migrate               # Run any pending migrations
just test                  # Run tests before committing

# Before pushing code
just format                # Format code
just lint                  # Check for issues
just test                  # Run all tests

# Working with database
just migration "add user table"  # Create migration
just migrate                     # Apply migration
just db-current                  # Check current state

# Docker workflow
just docker-build          # Build images
just docker-up             # Start services
just docker-logs backend   # Check backend logs
just docker-down           # Stop everything
```

### Migration from Make

The old `Makefile` has been replaced with a `justfile`. Key differences:

- **Commands**: `make format` → `just format`
- **Scope**: `just` commands work from the project root, not just backend/
- **Features**: More commands available with better organization
- **Cross-platform**: Better Windows support than Make

### Customization

Edit the `justfile` in the project root to add new commands or modify existing ones.

See the [just manual](https://just.systems/man/en/) for more advanced features.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
Free. No restrictions.
