# Backend

## Installation

### Prerequisites
- Python ^3.13.0
- [Poetry](https://python-poetry.org/) for dependency management
- [just](https://github.com/casey/just) command runner
- PostgreSQL (or use Docker)

### Setup
```bash
# Install Poetry (if not already installed)
pipx install poetry

# Install just (if not already installed)
brew install just  # macOS
# or follow installation guide: https://github.com/casey/just#installation

# Install dependencies (from project root)
just backend-install

# Or manually from backend directory
cd backend
poetry install
```

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure your environment:

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

Example `.env` file:
```bash
# Database Configuration (PostgreSQL)
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecpa_db

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
APP_ENV=development
```

## Database Setup

### Using Docker (Recommended)
```bash
# Start PostgreSQL in Docker (from project root)
just docker-up

# Run migrations
just db-upgrade
```

### Local PostgreSQL
1. Install PostgreSQL locally
2. Create a database named `ecpa_db`
3. Update `.env` with your credentials
4. Run migrations: `just db-upgrade`

## Development

### Common Commands
```bash
# Start development server
just backend-dev

# Run tests
just backend-test

# Format code
just backend-format

# Lint code
just backend-lint

# Type check
just backend-typecheck
```

## Database Migrations

### Using just commands (recommended)
```bash
# Create a new migration
just db-revision "description of changes"

# Upgrade database to latest
just db-upgrade

# Downgrade one migration
just db-downgrade

# Reset database (careful!)
just db-reset
```

### Manual Alembic commands
```bash
# Activate virtual environment
poetry shell

# Create new migration
alembic revision --autogenerate -m "description of changes"

# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1
```

## Debugging

### VS Code Debugging
1. Start backend in debug mode:
   ```bash
   just docker-debug
   ```

2. Use the "Backend: debug in docker" launch configuration in VS Code
3. Set breakpoints and press F5 to start debugging

## Optional
```bash
# Install pre-commit hooks
pre-commit install
```

For more commands and details, see the main [README.md](../README.md).
