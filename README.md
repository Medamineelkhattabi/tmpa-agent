# Oracle EBS R12 i-Supplier Assistant for Tanger Med

A full-stack AI-powered chatbot assistant designed to guide users through Oracle EBS R12 i-Supplier portal procedures with step-by-step instructions, contextual screenshots, and progress tracking.

## 🚀 Features

### Core Capabilities
- **Step-by-Step Guidance**: Interactive workflows for Oracle EBS R12 i-Supplier procedures
- **Contextual Screenshots**: Visual aids at each step to help users navigate the interface
- **Progress Tracking**: Real-time tracking of user progress through multi-step workflows
- **Oracle Module Queries**: Query purchase orders, invoices, and supplier information (mocked)
- **Rule-Based Responses**: Strictly follows predefined validated procedures
- **Session Management**: Persistent user sessions with workflow state

### Supported Procedures
1. **Create Work Confirmation** - Complete workflow for creating work confirmations
2. **Submit Invoice** - End-to-end invoice submission process
3. **View Purchase Orders** - Search and view purchase order information

### Technical Features
- **FastAPI Backend** - High-performance REST API
- **LangChain Integration** - Rule-based agent for procedure guidance
- **Modern Frontend** - Responsive HTML/CSS/JavaScript interface
- **Real-time Chat** - Interactive chat interface with suggestions
- **Screenshot Modal** - Full-screen screenshot viewing
- **Mobile Responsive** - Works on desktop, tablet, and mobile devices

## 🏗️ Architecture

```
oracle-ebs-assistant/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main FastAPI application
│   ├── models.py           # Pydantic data models
│   ├── oracle_agent.py     # LangChain-based agent
│   └── session_manager.py  # Session management
├── frontend/               # Frontend application
│   ├── index.html          # Main HTML interface
│   ├── styles.css          # CSS styling
│   └── app.js              # JavaScript application logic
├── static/images/          # Screenshot images
├── procedures.json         # Procedure definitions
└── requirements.txt        # Python dependencies
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js (for development server, optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd oracle-ebs-assistant
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   cd backend
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Serve the frontend**
   
   **Option A: Using Python's built-in server**
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   
   **Option B: Using Node.js (if installed)**
   ```bash
   cd frontend
   npx serve -s . -p 3000
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:3000`
   - The backend API will be running at `http://localhost:8000`

### Development Setup

For development with auto-reload:

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend (if using Node.js)
cd frontend
npx live-server --port=3000
```

## 📖 Usage Guide

### Starting a Procedure

1. **From Chat Interface**:
   - Type: "Start work confirmation"
   - Type: "Create work confirmation"
   - Use any of the suggested commands

2. **From Sidebar**:
   - Click the procedures button in the header
   - Select a procedure from the available list

### Following Procedure Steps

1. The assistant will guide you through each step
2. Read the instructions carefully
3. Click "View Screenshot" to see visual guidance
4. Type "done" or "next" when you complete each step
5. The assistant will validate completion and move to the next step

### Querying Oracle Data

- **Purchase Orders**: "Show purchase orders" or "Search PO-2024-001"
- **Invoices**: "List invoices" or "Show invoice status"
- **Suppliers**: "Search suppliers" or "Show supplier information"

### Session Management

- **View Progress**: Click the progress button to see current workflow status
- **Reset Session**: Click the reset button to start over
- **Session Persistence**: Your progress is maintained across browser refreshes

## 🔧 Configuration

### Adding New Procedures

Edit `procedures.json` to add new procedures:

```json
{
  "procedures": {
    "new_procedure": {
      "title": "New Procedure Title",
      "description": "Description of the procedure",
      "category": "category_name",
      "prerequisites": ["Prerequisite 1", "Prerequisite 2"],
      "steps": [
        {
          "step_id": "step_1",
          "title": "Step Title",
          "description": "Step description",
          "instructions": "Detailed instructions",
          "screenshot": "/static/images/screenshot.png",
          "validation_criteria": ["Criteria 1", "Criteria 2"],
          "next_steps": ["step_2"]
        }
      ]
    }
  }
}
```

### Adding Screenshots

1. Place screenshot images in `/static/images/`
2. Reference them in procedure steps using `/static/images/filename.png`
3. Use descriptive filenames for better organization

### Customizing Oracle Data

Modify the `mock_oracle_data` in `backend/oracle_agent.py` to add or change:
- Purchase orders
- Invoices
- Supplier information

## 🎨 Customization

### Styling
- Edit `frontend/styles.css` to customize the appearance
- The design uses CSS custom properties for easy theming
- Responsive breakpoints are defined for mobile compatibility

### Backend Configuration
- Modify `backend/main.py` for API endpoint changes
- Update `backend/models.py` for data structure modifications
- Customize `backend/oracle_agent.py` for business logic changes

## 🔒 Security Considerations

- **Input Validation**: All user inputs are validated
- **Session Security**: Session IDs are generated securely
- **CORS**: Configure CORS settings for production deployment
- **Rate Limiting**: Consider adding rate limiting for production use

## 🚀 Deployment

### Production Deployment

1. **Backend Deployment**:
   ```bash
   pip install gunicorn
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Frontend Deployment**:
   - Serve static files using nginx or Apache
   - Update API base URL in `frontend/app.js`

3. **Environment Variables**:
   ```bash
   export ENVIRONMENT=production
   export API_BASE_URL=https://your-api-domain.com
   ```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Backend won't start**:
   - Check Python version (3.8+ required)
   - Verify all dependencies are installed
   - Check port 8000 is available

2. **Frontend can't connect to backend**:
   - Verify backend is running on port 8000
   - Check CORS configuration
   - Update API base URL if needed

3. **Screenshots not loading**:
   - Verify image files exist in `/static/images/`
   - Check file permissions
   - Ensure correct file paths in procedures.json

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export DEBUG=true
```

## 📝 API Documentation

### Endpoints

- `POST /api/chat` - Send chat message
- `GET /api/procedures` - Get available procedures
- `GET /api/procedures/{id}` - Get procedure details
- `POST /api/oracle/query` - Query Oracle modules
- `GET /api/session/{id}/progress` - Get session progress
- `POST /api/session/{id}/reset` - Reset session

### WebSocket Support (Future)

WebSocket support can be added for real-time updates:
```python
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    # Real-time chat implementation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section above

---

**Note**: This is a demonstration application. For production use with real Oracle EBS systems, additional security measures, authentication, and integration with actual Oracle APIs would be required.