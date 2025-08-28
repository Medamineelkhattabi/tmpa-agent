# Oracle EBS R12 Assistant - Docker Deployment Guide

## 🐳 Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum
- 5GB disk space

### Development Deployment
```bash
# Make script executable (Linux/Mac)
chmod +x docker-run.sh

# Start development environment
./docker-run.sh dev

# Access application
open http://localhost:8000
```

### Windows Deployment
```cmd
# Build and run
docker-compose up --build -d

# Access application
start http://localhost:8000
```

## 📋 Available Commands

### Using the deployment script:
```bash
./docker-run.sh dev     # Development mode
./docker-run.sh prod    # Production mode
./docker-run.sh stop    # Stop all services
./docker-run.sh logs    # View logs
./docker-run.sh clean   # Clean up resources
```

### Manual Docker commands:
```bash
# Development
docker-compose up --build -d
docker-compose logs -f
docker-compose down

# Production
docker-compose -f docker-compose.prod.yml up --build -d
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml down
```

## 🏗️ Architecture

### Development Stack
```
┌─────────────────────┐
│   Oracle EBS        │
│   Assistant         │ :8000
│   (FastAPI)         │
└─────────────────────┘
```

### Production Stack
```
┌─────────────────────┐
│      Nginx          │ :80, :443
│   (Load Balancer)   │
└─────────────────────┘
           │
┌─────────────────────┐
│   Oracle EBS        │
│   Assistant         │ :8000
│   (FastAPI)         │
└─────────────────────┘
           │
┌─────────────────────┐
│      Redis          │ :6379
│   (Session Store)   │
└─────────────────────┘
           │
┌─────────────────────┐
│    PostgreSQL       │ :5432
│   (Database)        │
└─────────────────────┘
```

## ⚙️ Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your values
```

### Key Configuration Options:
- `GOOGLE_API_KEY`: Required for AI functionality
- `POSTGRES_*`: Database credentials (production)
- `REDIS_PASSWORD`: Redis authentication (production)
- `WORKERS`: Number of FastAPI workers

## 🔧 Customization

### Adding Custom Procedures
1. Edit `procedures.json`
2. Rebuild container: `docker-compose up --build`

### Modifying Frontend
1. Edit files in `frontend/`
2. Rebuild: `docker-compose up --build`

### Adding Environment Variables
1. Add to `.env` file
2. Update `docker-compose.yml`
3. Restart services

## 📊 Monitoring

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f oracle-ebs-assistant

# Production logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Health Checks
```bash
# Check service status
docker-compose ps

# Health check endpoint
curl http://localhost:8000/

# Container health
docker inspect oracle-ebs-assistant --format='{{.State.Health.Status}}'
```

## 🚀 Production Deployment

### 1. Prepare Environment
```bash
# Copy and configure environment
cp .env.example .env
nano .env  # Configure your values

# Ensure SSL certificates (if using HTTPS)
mkdir ssl
# Copy your cert.pem and key.pem to ssl/
```

### 2. Deploy
```bash
# Start production stack
./docker-run.sh prod

# Or manually
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Verify Deployment
```bash
# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Test application
curl http://localhost/
```

## 🔒 Security Features

### Built-in Security:
- Non-root container user
- Input sanitization
- Rate limiting
- CORS protection
- Security headers
- Health checks

### Production Security:
- SSL/TLS encryption (with nginx)
- Database authentication
- Redis password protection
- Resource limits
- Network isolation

## 🛠️ Troubleshooting

### Common Issues:

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill process or change port in docker-compose.yml
```

#### Permission Denied
```bash
# Fix script permissions
chmod +x docker-run.sh
```

#### Out of Memory
```bash
# Increase Docker memory limit
# Or reduce workers in .env file
WORKERS=1
```

#### Container Won't Start
```bash
# Check logs
docker-compose logs oracle-ebs-assistant

# Check container status
docker ps -a
```

### Debug Mode
```bash
# Run with debug output
DEBUG=true docker-compose up

# Access container shell
docker exec -it oracle-ebs-assistant bash
```

## 📈 Performance Tuning

### Resource Limits
Edit `docker-compose.prod.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
```

### Worker Configuration
Adjust in `.env`:
```bash
WORKERS=4  # CPU cores * 2
MAX_REQUESTS=1000
TIMEOUT=30
```

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up --build -d
```

### Backup Data
```bash
# Backup volumes
docker run --rm -v oracle_ebs_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz /data

# Backup procedures
cp procedures.json procedures-backup.json
```

### Clean Up
```bash
# Remove unused resources
./docker-run.sh clean

# Or manually
docker system prune -a
```

## 📞 Support

For issues and questions:
1. Check logs: `docker-compose logs -f`
2. Verify configuration: `docker-compose config`
3. Test connectivity: `curl http://localhost:8000/`
4. Review this documentation

## 🎯 Next Steps

After successful deployment:
1. Configure SSL certificates for production
2. Set up monitoring and alerting
3. Configure backup strategies
4. Integrate with real Oracle EBS system
5. Set up CI/CD pipeline