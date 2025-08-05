# Quick Start & Deployment Guide

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
./start.sh
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

That's it! The Oracle EBS Assistant is now running.

## 🧪 Testing the Application

### Command Line Demo
```bash
# Interactive chat demo
python3 demo.py

# Automated demo
python3 demo.py auto

# Show available procedures
python3 demo.py procedures

# Show sample Oracle data
python3 demo.py data
```

### Web Interface Testing
1. Open http://localhost:3000 in your browser
2. Try these commands:
   - "help"
   - "start work confirmation"
   - "show purchase orders"
   - "list invoices"

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t oracle-ebs-assistant .
```

### Run with Docker
```bash
docker run -p 8000:8000 oracle-ebs-assistant
```

### Docker Compose (Full Stack)
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
  
  frontend:
    image: nginx:alpine
    ports:
      - "3000:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
```

## 🌐 Production Deployment

### Backend (FastAPI)
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (Static Files)
```bash
# Serve with nginx
sudo cp -r frontend/* /var/www/html/
sudo systemctl restart nginx
```

### Environment Variables
```bash
export DEBUG=false
export HOST=0.0.0.0
export PORT=8000
export API_BASE_URL=https://your-domain.com/api
```

## 🔧 Configuration

### Custom Procedures
Edit `procedures.json` to add your own Oracle EBS procedures.

### Custom Oracle Data
Modify `backend/oracle_agent.py` to connect to real Oracle EBS systems.

### Styling
Customize `frontend/styles.css` for your organization's branding.

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/
```

### API Status
```bash
curl http://localhost:8000/docs
```

### Logs
```bash
tail -f logs/backend.log
tail -f logs/frontend.log
```

## 🔒 Security Checklist

- [ ] Configure CORS for production domains
- [ ] Add authentication if required
- [ ] Set up HTTPS certificates
- [ ] Configure rate limiting
- [ ] Validate all user inputs
- [ ] Secure Oracle EBS connections

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Kill processes on port 8000
sudo lsof -ti:8000 | xargs kill -9

# Kill processes on port 3000
sudo lsof -ti:3000 | xargs kill -9
```

### Dependencies Issues
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Not Loading
- Check if backend is running on port 8000
- Verify CORS configuration
- Check browser console for errors

## 📈 Performance Tuning

### Backend Optimization
- Use Redis for session storage
- Implement caching for procedures
- Add database connection pooling

### Frontend Optimization
- Minify CSS and JavaScript
- Implement service worker for caching
- Use CDN for static assets

## 🔄 Updates & Maintenance

### Updating Procedures
1. Edit `procedures.json`
2. Restart the backend server
3. Changes take effect immediately

### Adding Screenshots
1. Add images to `static/images/`
2. Update procedure definitions
3. No restart required

### Database Migration (Future)
When moving from in-memory to database storage:
1. Set up PostgreSQL/MySQL
2. Update `backend/session_manager.py`
3. Run migration scripts

---

**Need Help?** Check the main README.md for detailed documentation.