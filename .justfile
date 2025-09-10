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
    @echo "📦 Installing backend dependencies to root .venv..."
    source .venv/bin/activate && uv pip install -e "./{{backend_dir}}[dev]"
    @echo "📦 Installing frontend dependencies..."
    cd {{frontend_dir}} && npm install
    @echo "📋 Updating requirements files..."
    just update-requirements
    @echo "💡 IDE Python interpreter path: .venv/bin/python"

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
    cd {{backend_dir}} && ../.venv/bin/python -m pytest

# Run backend tests with coverage
test-coverage:
    @echo "📊 Running backend tests with coverage..."
    cd {{backend_dir}} && ../.venv/bin/python -m pytest --cov=app --cov-report=html --cov-report=term

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

# ============================================================================
# Docker Commands
# ============================================================================

docker +args='':
    docker-compose -f {{docker_dir}}/docker-compose.yml -f {{docker_dir}}/docker-compose-frontend.yml {{args}}

docker-debug +args='':
    docker-compose -f {{docker_dir}}/docker-compose.yml -f {{docker_dir}}/docker-compose-debug.yml -f {{docker_dir}}/docker-compose-frontend.yml {{args}}

# View Docker logs
docker-logs +args='':
    @echo "📋 Viewing Docker logs..."
    docker-compose -f {{docker_dir}}/docker-compose.yml logs {{args}} 

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

# Update requirements files
update-requirements:
    @echo "📋 Updating requirements files..."
    cd {{backend_dir}} && uv export --no-dev --format requirements-txt --no-hashes --no-emit-project > requirements.txt
    cd {{backend_dir}} && uv export --format requirements-txt --no-hashes --no-emit-project > requirements-dev.txt
    @echo "✅ Requirements files updated!"

# Force update and sync all (may break IDE)
update-full:
    @echo "⬆️  Force updating ALL dependencies (may break IDE)..."
    cd {{backend_dir}} && uv lock --upgrade
    cd {{backend_dir}} && uv sync --all-extras
    cd {{frontend_dir}} && npm update
    @echo "💡 IDE Python interpreter path: .venv/bin/python"

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