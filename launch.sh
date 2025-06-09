#!/bin/bash

# Crypto Strategy Analyzer Launcher
# Supports multiple deployment platforms

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect platform
detect_platform() {
    if [[ -n "$HEROKU_APP_NAME" ]]; then
        echo "heroku"
    elif [[ -n "$GITHUB_ACTIONS" ]]; then
        echo "github"
    elif [[ -n "$STREAMLIT_SHARING" ]]; then
        echo "streamlit"
    elif [[ -f "/.dockerenv" ]]; then
        echo "docker"
    else
        echo "local"
    fi
}

# Check Python version
check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        exit 1
    fi

    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    required_version="3.9"

    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
        log_success "Python ${python_version} detected"
    else
        log_error "Python ${required_version}+ required, but ${python_version} found"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    log_info "Installing dependencies..."

    if [[ -f "requirements.txt" ]]; then
        pip install --no-cache-dir -r requirements.txt
        log_success "Dependencies installed"
    else
        log_error "requirements.txt not found"
        exit 1
    fi
}

# Run initial analysis
run_initial_analysis() {
    log_info "Running initial crypto analysis..."

    if python3 data_processor.py; then
        log_success "Initial analysis completed"
    else
        log_warning "Initial analysis failed, but continuing..."
    fi
}

# Start the application
start_application() {
    local platform=$1
    local port=${PORT:-8501}

    log_info "Starting application for platform: ${platform}"

    case $platform in
        "heroku")
            exec streamlit run enhanced_app.py \
                --server.port=$port \
                --server.address=0.0.0.0 \
                --server.headless=true \
                --server.enableCORS=false \
                --server.enableXsrfProtection=false
            ;;
        "docker")
            exec streamlit run enhanced_app.py \
                --server.port=8501 \
                --server.address=0.0.0.0 \
                --server.headless=true \
                --server.enableCORS=false \
                --server.enableXsrfProtection=false
            ;;
        "github"|"streamlit")
            exec streamlit run enhanced_app.py \
                --server.headless=true
            ;;
        "local"|*)
            exec streamlit run enhanced_app.py
            ;;
    esac
}

# Main function
main() {
    log_info "🚀 Crypto Strategy Analyzer Launcher"

    # Detect platform
    platform=$(detect_platform)
    log_info "Detected platform: ${platform}"

    # Check Python
    check_python

    # Set environment
    export ENVIRONMENT=${ENVIRONMENT:-production}
    export DATA_START_DATE=${DATA_START_DATE:-2018-01-01}

    # For production platforms, install dependencies
    if [[ "$platform" != "local" ]]; then
        install_dependencies
    fi

    # Run initial analysis (except for local development)
    if [[ "$platform" != "local" ]] && [[ ! -f "strategy_results.json" ]]; then
        run_initial_analysis
    fi

    # Start application
    start_application $platform
}

# Handle command line arguments
case "${1:-}" in
    "--help"|"-h")
        echo "Crypto Strategy Analyzer Launcher"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --check        Check system requirements"
        echo "  --analyze      Run analysis only"
        echo "  --no-analysis  Skip initial analysis"
        echo ""
        echo "Environment Variables:"
        echo "  PORT                Application port (default: 8501)"
        echo "  ENVIRONMENT         Runtime environment (development/production)"
        echo "  DATA_START_DATE     Analysis start date (default: 2018-01-01)"
        echo ""
        exit 0
        ;;
    "--check")
        log_info "Checking system requirements..."
        check_python

        if command -v streamlit &> /dev/null; then
            streamlit_version=$(streamlit version | head -n1)
            log_success "Streamlit: ${streamlit_version}"
        else
            log_error "Streamlit not installed"
        fi

        if [[ -f "requirements.txt" ]]; then
            log_success "requirements.txt found"
        else
            log_error "requirements.txt not found"
        fi

        if [[ -f "enhanced_app.py" ]]; then
            log_success "enhanced_app.py found"
        else
            log_error "enhanced_app.py not found"
        fi

        exit 0
        ;;
    "--analyze")
        log_info "Running analysis only..."
        check_python
        python3 data_processor.py
        log_success "Analysis completed"
        exit 0
        ;;
    "--no-analysis")
        log_info "Skipping initial analysis..."
        export SKIP_ANALYSIS=true
        ;;
esac

# Run main function
main
