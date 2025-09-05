# justfile for ECPA project
# Run `just --list` to see all available commands

# Set shell to use
set shell := ["zsh", "-c"]

# Variables
backend_dir := "backend"
frontend_dir := "frontend"
docker_dir := "docker"

# Show all available commands
default:
    @just --list

# ============================================================================
# Development Commands
# ============================================================================

install:
    @echo "📦 Installing ALL backend dependencies (may break IDE)..."
    cd {{backend_dir}} && uv sync --all-extras
    @echo "📦 Installing frontend dependencies..."
    cd {{frontend_dir}} && npm install
    @echo "💡 IDE Python interpreter path: {{backend_dir}}/.venv/bin/python"

# Start the development servers
dev:
    @echo "🚀 Starting development servers..."
    just dev-backend &
    just dev-frontend &
    wait

# Start backend development server
dev-backend:
    @echo "🐍 Starting FastAPI backend server..."
    cd {{backend_dir}} && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend development server
dev-frontend:
    @echo "⚛️  Starting Next.js frontend server..."
    cd {{frontend_dir}} && npm run dev

# ============================================================================
# Database Commands
# ============================================================================

# Run database migrations
migrate:
    @echo "🗄️  Running database migrations..."
    cd {{backend_dir}} && uv run alembic upgrade head

# Create a new migration
migration message:
    @echo "📝 Creating new migration: {{message}}"
    cd {{backend_dir}} && uv run alembic revision --autogenerate -m "{{message}}"

# Reset database (down and up)
db-reset:
    @echo "♻️  Resetting database..."
    cd {{backend_dir}} && uv run alembic downgrade base
    cd {{backend_dir}} && uv run alembic upgrade head

# Show migration history
db-history:
    @echo "📜 Database migration history:"
    cd {{backend_dir}} && uv run alembic history

# Show current database revision
db-current:
    @echo "📍 Current database revision:"
    cd {{backend_dir}} && uv run alembic current

# ============================================================================
# Testing Commands
# ============================================================================

# Run all tests
test:
    @echo "🧪 Running all tests..."
    just test-backend
    just test-frontend

# Run backend tests
test-backend:
    @echo "🐍 Running backend tests..."
    cd {{backend_dir}} && uv run pytest

# Run backend tests with coverage
test-coverage:
    @echo "📊 Running backend tests with coverage..."
    cd {{backend_dir}} && uv run pytest --cov=app --cov-report=html --cov-report=term

# Run frontend tests
test-frontend:
    @echo "⚛️  Running frontend tests..."
    cd {{frontend_dir}} && npm test

# ============================================================================
# Code Quality Commands
# ============================================================================

# Format all code
format:
    @echo "🎨 Formatting code..."
    just format-backend
    just format-frontend

# Format backend code
format-backend:
    @echo "🐍 Formatting backend code..."
    cd {{backend_dir}} && uv run ruff check --fix .
    cd {{backend_dir}} && uv run ruff format .

# Format frontend code
format-frontend:
    @echo "⚛️  Formatting frontend code..."
    cd {{frontend_dir}} && npm run format

# Lint all code
lint:
    @echo "🔍 Linting code..."
    just lint-backend
    just lint-frontend

# Lint backend code
lint-backend:
    @echo "🐍 Linting backend code..."
    cd {{backend_dir}} && uv run ruff check .
    cd {{backend_dir}} && uv run mypy .

# Lint frontend code
lint-frontend:
    @echo "⚛️  Linting frontend code..."
    cd {{frontend_dir}} && npm run lint

# Fix linting issues
fix:
    @echo "🔧 Fixing linting issues..."
    cd {{backend_dir}} && uv run ruff check --fix .
    cd {{frontend_dir}} && npm run lint:fix

# ============================================================================
# Docker Commands
# ============================================================================

docker +args='':
    docker-compose -f {{docker_dir}}/docker-compose.yml -f {{docker_dir}}/docker-compose-frontend.yml {{args}}

docker-debug +args='':
    docker-compose -f {{docker_dir}}/docker-compose.yml -f {{docker_dir}}/docker-compose-debug.yml -f {{docker_dir}}/docker-compose-frontend.yml {{args}}

# Build all Docker images
docker-build:
    @echo "🐳 Building Docker images..."
    just docker-build-backend
    just docker-build-frontend

# Build backend Docker image
docker-build-backend:
    @echo "🐳 Building backend Docker image..."
    docker-compose -f {{docker_dir}}/docker-compose.yml build backend

# Build frontend Docker image
docker-build-frontend:
    @echo "🐳 Building frontend Docker image..."
    docker-compose -f {{docker_dir}}/docker-compose.yml -f {{docker_dir}}/docker-compose-frontend.yml build frontend

# Start all services with Docker
docker-up:
    @echo "🐳 Starting Docker services..."
    just docker-up-backend
    just docker-up-frontend

# Start backend with Docker
docker-up-backend:
    @echo "🐳 Starting backend Docker services..."
    docker-compose -f {{docker_dir}}/docker-compose.yml up -d

# Start frontend with Docker (requires backend to be running)
docker-up-frontend:
    @echo "🐳 Starting frontend Docker service..."
    docker-compose -f {{docker_dir}}/docker-compose.yml -f {{docker_dir}}/docker-compose-frontend.yml up frontend -d

# Stop all Docker services
docker-down:
    @echo "🐳 Stopping Docker services..."
    just docker-down-frontend
    just docker-down-backend

# Stop backend Docker services
docker-down-backend:
    @echo "🐳 Stopping backend Docker services..."
    docker-compose -f {{docker_dir}}/docker-compose.yml down

# Stop frontend Docker service
docker-down-frontend:
    @echo "🐳 Stopping frontend Docker service..."
    docker-compose -f {{docker_dir}}/docker-compose.yml -f {{docker_dir}}/docker-compose-frontend.yml stop frontend

# View Docker logs
docker-logs service="":
    @echo "📋 Viewing Docker logs..."
    docker-compose -f {{docker_dir}}/docker-compose.yml logs {{service}}

# Restart Docker services
docker-restart:
    @echo "♻️  Restarting Docker services..."
    just docker-down
    just docker-up

# ============================================================================
# Utility Commands
# ============================================================================

# Clean up temporary files and caches
clean:
    @echo "🧹 Cleaning up..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true

# Show project status
status:
    @echo "📊 Project Status:"
    @echo "Backend directory: {{backend_dir}}"
    @echo "Frontend directory: {{frontend_dir}}"
    @echo "Docker directory: {{docker_dir}}"
    @echo ""
    @echo "🐍 Backend dependencies:"
    cd {{backend_dir}} && uv pip list | head -10
    @echo ""
    @echo "⚛️  Frontend dependencies:"
    cd {{frontend_dir}} && npm list --depth=0 2>/dev/null | head -10 || echo "Run 'npm install' first"

# Update all dependencies (IDE-safe)
update:
    @echo "⬆️  Updating dependencies..."
    cd {{backend_dir}} && uv lock --upgrade
    cd {{backend_dir}} && uv sync --no-progress --frozen
    cd {{frontend_dir}} && npm update

# Force update and sync all (may break IDE)
update-full:
    @echo "⬆️  Force updating ALL dependencies (may break IDE)..."
    cd {{backend_dir}} && uv lock --upgrade
    cd {{backend_dir}} && uv sync --all-extras
    cd {{frontend_dir}} && npm update
    @echo "💡 IDE Python interpreter path: {{backend_dir}}/.venv/bin/python"

# Check for security vulnerabilities
security:
    @echo "🔒 Checking for security vulnerabilities..."
    cd {{backend_dir}} && uv run safety check
    cd {{frontend_dir}} && npm audit

# Generate API documentation
docs:
    @echo "📚 Generating API documentation..."
    @echo "FastAPI docs available at: http://localhost:8000/docs"
    @echo "Redoc available at: http://localhost:8000/redoc"

# Setup development environment
setup:
    @echo "🛠️  Setting up development environment..."
    just install
    just migrate
    @echo "✅ Development environment ready!"
    @echo "Run 'just dev' to start development servers"

# ============================================================================
# Git Hooks (if using pre-commit)
# ============================================================================

# Install pre-commit hooks
hooks-install:
    @echo "🪝 Installing pre-commit hooks..."
    cd {{backend_dir}} && uv run pre-commit install

# Run pre-commit hooks manually
hooks-run:
    @echo "🪝 Running pre-commit hooks..."
    cd {{backend_dir}} && uv run pre-commit run --all-files

# ============================================================================
# Production Commands
# ============================================================================

# Build for production
build:
    @echo "🏗️  Building for production..."
    cd {{frontend_dir}} && npm run build
    cd {{backend_dir}} && uv build

# Start production server (backend only)
start:
    @echo "🚀 Starting production server..."
    cd {{backend_dir}} && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
