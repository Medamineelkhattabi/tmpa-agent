#!/bin/bash
# Docker deployment script for Oracle EBS R12 Assistant

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "  Oracle EBS R12 Assistant - Docker Deployment"
    echo "=================================================="
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are installed"
}

# Build and run the application
run_development() {
    print_header
    echo "🚀 Starting Oracle EBS Assistant in Development Mode..."
    
    check_docker
    
    # Build and start services
    docker-compose down --remove-orphans
    docker-compose build --no-cache
    docker-compose up -d
    
    # Wait for services to be ready
    echo "⏳ Waiting for services to start..."
    sleep 10
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Oracle EBS Assistant is running!"
        echo ""
        echo "🌐 Access the application at:"
        echo "   http://localhost:8000"
        echo "   http://localhost:8000/advanced/"
        echo ""
        echo "📊 View logs with:"
        echo "   docker-compose logs -f"
        echo ""
        echo "🛑 Stop with:"
        echo "   docker-compose down"
    else
        print_error "Failed to start services. Check logs with: docker-compose logs"
        exit 1
    fi
}

# Run production deployment
run_production() {
    print_header
    echo "🏭 Starting Oracle EBS Assistant in Production Mode..."
    
    check_docker
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        print_warning "Creating .env file with default values..."
        cat > .env << EOF
GOOGLE_API_KEY=AIzaSyC8pw11h7ppDilnA-ITc8-SmF8daANOhIw
POSTGRES_DB=oracle_ebs_assistant
POSTGRES_USER=oracle_user
POSTGRES_PASSWORD=oracle_secure_password_123
REDIS_PASSWORD=redis_secure_password_123
EOF
        print_warning "Please update .env file with your actual credentials!"
    fi
    
    # Build and start production services
    docker-compose -f docker-compose.prod.yml down --remove-orphans
    docker-compose -f docker-compose.prod.yml build --no-cache
    docker-compose -f docker-compose.prod.yml up -d
    
    # Wait for services
    echo "⏳ Waiting for production services to start..."
    sleep 15
    
    if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        print_success "Oracle EBS Assistant Production is running!"
        echo ""
        echo "🌐 Access the application at:"
        echo "   http://localhost"
        echo ""
        echo "📊 Monitor with:"
        echo "   docker-compose -f docker-compose.prod.yml logs -f"
    else
        print_error "Failed to start production services"
        exit 1
    fi
}

# Show usage
show_usage() {
    echo "Usage: $0 [dev|prod|stop|logs|clean]"
    echo ""
    echo "Commands:"
    echo "  dev     - Start in development mode"
    echo "  prod    - Start in production mode"
    echo "  stop    - Stop all services"
    echo "  logs    - Show application logs"
    echo "  clean   - Clean up Docker resources"
    echo ""
}

# Stop services
stop_services() {
    echo "🛑 Stopping Oracle EBS Assistant services..."
    docker-compose down --remove-orphans
    docker-compose -f docker-compose.prod.yml down --remove-orphans
    print_success "Services stopped"
}

# Show logs
show_logs() {
    echo "📊 Showing Oracle EBS Assistant logs..."
    if docker-compose ps | grep -q "Up"; then
        docker-compose logs -f
    elif docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        docker-compose -f docker-compose.prod.yml logs -f
    else
        print_warning "No running services found"
    fi
}

# Clean up Docker resources
clean_docker() {
    echo "🧹 Cleaning up Docker resources..."
    docker-compose down --remove-orphans --volumes
    docker-compose -f docker-compose.prod.yml down --remove-orphans --volumes
    docker system prune -f
    print_success "Docker cleanup completed"
}

# Main script logic
case "$1" in
    "dev")
        run_development
        ;;
    "prod")
        run_production
        ;;
    "stop")
        stop_services
        ;;
    "logs")
        show_logs
        ;;
    "clean")
        clean_docker
        ;;
    *)
        show_usage
        exit 1
        ;;
esac