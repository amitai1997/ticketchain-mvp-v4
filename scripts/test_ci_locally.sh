#!/bin/bash
set -e

echo "🧪 Testing CI-like conditions locally"
echo "======================================"

# Test Poetry installation and configuration
echo "📦 Testing Poetry setup..."
if command -v poetry >/dev/null 2>&1; then
    echo "✅ Poetry is installed: $(poetry --version)"

    # Test Poetry configuration
    echo "📋 Poetry configuration:"
    poetry config --list | grep -E "(virtualenvs|cache)"

    # Test Poetry lock file validity
    echo "🔒 Validating Poetry lock file..."
    poetry check

    # Test dependency installation in clean environment
    echo "📥 Testing dependency installation..."
    poetry install --dry-run

else
    echo "❌ Poetry not found - install it first"
    exit 1
fi

# Test Python/MyPy setup
echo "🐍 Testing Python type checking..."
poetry run mypy src || {
    echo "❌ MyPy type checking failed"
    exit 1
}

# Test all linting tools like CI
echo "🔍 Testing code quality checks..."
poetry run ruff check src tests || {
    echo "❌ Ruff linting failed"
    exit 1
}

poetry run black --check src tests || {
    echo "❌ Black formatting check failed"
    exit 1
}

# Test basic unit tests
echo "🧪 Testing Python unit tests..."
poetry run pytest tests/unit/ --tb=short || {
    echo "❌ Unit tests failed"
    exit 1
}

# Test Node.js/npm setup
echo "📦 Testing Node.js setup..."
if command -v npm >/dev/null 2>&1; then
    echo "✅ npm is available: $(npm --version)"

    # Test package installation
    echo "📥 Testing npm dependencies..."
    npm ci --dry-run || {
        echo "❌ npm dependency check failed"
        exit 1
    }

    # Test artifacts directory permissions (CI-like check)
    echo "📁 Testing artifacts directory permissions..."
    if [ -d "artifacts" ]; then
        echo "✅ artifacts directory exists"
    else
        echo "📂 Creating artifacts directory structure..."
        mkdir -p artifacts/build-info artifacts/contracts || {
            echo "❌ Cannot create artifacts directory - permission issue"
            exit 1
        }
    fi

    # Test write permissions
    touch artifacts/test-write.tmp && rm artifacts/test-write.tmp || {
        echo "❌ No write permission to artifacts directory"
        exit 1
    }
    echo "✅ artifacts directory is writable"

    # Test Hardhat compilation
    echo "🔨 Testing contract compilation..."
    npx hardhat compile || {
        echo "❌ Contract compilation failed"
        exit 1
    }

    # Test smart contract tests
    echo "🧪 Testing smart contract tests..."
    npx hardhat test || {
        echo "❌ Smart contract tests failed"
        exit 1
    }

else
    echo "❌ npm not found - install Node.js first"
    exit 1
fi

# Test Docker setup (if available)
if command -v docker >/dev/null 2>&1; then
    echo "🐳 Testing Docker availability..."
    docker --version

            if docker compose version >/dev/null 2>&1; then
        echo "✅ Docker Compose V2 is available"
        DOCKER_COMPOSE_CMD=("docker" "compose")
    elif command -v docker-compose >/dev/null 2>&1; then
        echo "✅ Docker Compose V1 is available"
        DOCKER_COMPOSE_CMD=("docker-compose")
    else
        echo "⚠️  Docker Compose not available - integration tests may fail in CI"
        DOCKER_COMPOSE_CMD=()
    fi

    if [ ${#DOCKER_COMPOSE_CMD[@]} -gt 0 ]; then
        # Test Docker Compose configuration
        echo "📋 Validating Docker Compose configuration..."
        "${DOCKER_COMPOSE_CMD[@]}" config >/dev/null || {
            echo "❌ Docker Compose configuration invalid"
            exit 1
        }
    else
        echo "⚠️  Docker Compose not available - integration tests may fail in CI"
    fi
else
    echo "⚠️  Docker not available - integration tests may fail in CI"
fi

# Test environment variable setup
echo "🌍 Testing environment configuration..."
if [ -f .env.example ]; then
    echo "✅ .env.example found"

    # Check for common required environment variables
    missing_vars=()
    while IFS= read -r line; do
        if [[ $line =~ ^[A-Z_]+=.* ]]; then
            var_name=$(echo "$line" | cut -d'=' -f1)
            if [ -z "${!var_name}" ]; then
                missing_vars+=("$var_name")
            fi
        fi
    done < .env.example

    if [ ${#missing_vars[@]} -gt 0 ]; then
        echo "⚠️  Missing environment variables (set in .env or shell):"
        printf "   - %s\n" "${missing_vars[@]}"
    else
        echo "✅ All example environment variables are set"
    fi
else
    echo "⚠️  .env.example not found"
fi

echo ""
echo "🎉 Local CI simulation completed successfully!"
echo ""
echo "💡 This script tests most CI conditions locally, but some issues are CI-specific:"
echo "   - Network connectivity problems (SSL/TLS issues)"
echo "   - GitHub Actions runner environment differences"
echo "   - Docker service startup timing in CI"
echo ""
echo "📚 To run this regularly, add to package.json scripts:"
echo "   \"test:ci-local\": \"./scripts/test_ci_locally.sh\""
