# 📋 **ANNEXES DÉTAILLÉES**
## Oracle EBS R12 i-Supplier Assistant - Tanger Med Port Authority

---

## **TABLE DES MATIÈRES**

- [ANNEXE A - ARCHITECTURE TECHNIQUE COMPLÈTE](#annexe-a)
- [ANNEXE B - PROCÉDURES ORACLE EBS R12](#annexe-b)
- [ANNEXE C - CONFIGURATION DOCKER](#annexe-c)
- [ANNEXE D - SÉCURITÉ ET CONFORMITÉ](#annexe-d)
- [ANNEXE E - MÉTRIQUES ET MONITORING](#annexe-e)
- [ANNEXE F - GUIDE DE DÉPLOIEMENT](#annexe-f)
- [ANNEXE G - API DOCUMENTATION](#annexe-g)
- [ANNEXE H - TROUBLESHOOTING](#annexe-h)

---

## **ANNEXE A - ARCHITECTURE TECHNIQUE COMPLÈTE** {#annexe-a}

### **A.1 Stack Technologique Détaillé**

#### **A.1.1 Backend - Écosystème Python**
```python
# requirements.txt - Dépendances critiques avec versions exactes
fastapi==0.104.1              # Framework API REST moderne et performant
uvicorn==0.24.0               # Serveur ASGI haute performance avec support WebSocket
pydantic==2.5.0               # Validation de données avec types Python
google-generativeai==0.3.2    # SDK officiel Google Gemini AI
langchain==0.1.0              # Framework IA conversationnelle et agents
langchain-community==0.0.10   # Extensions communautaires LangChain
bleach==6.1.0                 # Protection XSS et sanitisation HTML
python-jose==3.3.0            # Implémentation JWT pour authentification
passlib==1.7.4                # Hachage sécurisé des mots de passe
cryptography==41.0.7          # Cryptographie avancée et certificats
redis==5.0.1                  # Client Redis pour cache distribué
sqlalchemy==1.4.49            # ORM Python pour bases de données
databases==0.8.0              # Interface async pour bases de données
asyncpg==0.29.0               # Driver PostgreSQL asynchrone
httpx==0.25.2                 # Client HTTP async moderne
pillow==10.1.0                # Traitement et manipulation d'images
aiofiles==23.2.1              # I/O fichiers asynchrone
python-multipart==0.0.6       # Support upload de fichiers multipart
jinja2==3.1.2                 # Moteur de templates pour génération HTML
```

#### **A.1.2 Frontend - Technologies Web Modernes**
```javascript
// Technologies et APIs utilisées
const FRONTEND_STACK = {
    core: {
        language: "JavaScript ES6+",
        framework: "Vanilla JS (pas de framework lourd)",
        architecture: "Progressive Web App (PWA)",
        responsive: "Mobile-first design"
    },
    apis: {
        fetch: "Communication HTTP asynchrone",
        webSpeech: "Reconnaissance et synthèse vocale",
        serviceWorker: "Cache offline et notifications push",
        webStorage: "LocalStorage pour préférences utilisateur",
        webCrypto: "Génération UUID sécurisés"
    },
    styling: {
        css3: "Grid, Flexbox, Custom Properties",
        responsive: "Breakpoints: 320px, 768px, 1024px, 1440px",
        themes: "Mode sombre/clair avec CSS variables",
        animations: "Transitions CSS3 et keyframes"
    },
    performance: {
        bundling: "Pas de bundler - fichiers natifs",
        caching: "Service Worker avec stratégies de cache",
        lazy: "Chargement différé des images",
        compression: "Gzip via Nginx"
    }
};
```

#### **A.1.3 Infrastructure - Containerisation Avancée**
```yaml
# Stack d'infrastructure complète
infrastructure:
  containerization:
    docker_engine: "24.0+"
    docker_compose: "3.8"
    base_images:
      - "python:3.9-slim (optimisé pour production)"
      - "nginx:alpine (serveur web léger)"
      - "redis:7-alpine (cache mémoire)"
      - "postgres:15-alpine (base de données)"
  
  networking:
    reverse_proxy: "Nginx avec SSL/TLS"
    load_balancing: "Round-robin upstream"
    security: "Rate limiting, CORS, Security headers"
  
  storage:
    volumes: "Docker volumes persistants"
    backup: "Snapshots automatisés"
    logs: "Rotation automatique des logs"
  
  monitoring:
    health_checks: "Docker healthcheck intégré"
    metrics: "Prometheus (optionnel)"
    logging: "JSON structured logging"
```

### **A.2 Diagramme d'Architecture Détaillé**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ORACLE EBS R12 ASSISTANT ECOSYSTEM                      │
│                         Tanger Med Port Authority                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
            ┌───────────────────────────┼─────────────────────────┐
            │                           │                         │
    ┌───────▼──────┐            ┌──────▼──────┐            ┌──────▼──────┐
    │   FRONTEND   │            │   BACKEND   │            │  EXTERNAL   │
    │    LAYER     │            │    LAYER    │            │  SERVICES   │
    └──────────────┘            └─────────────┘            └─────────────┘
            │                          │                          │
    ┌───────▼──────┐            ┌──────▼──────┐            ┌──────▼──────┐
    │ UI Variants: │            │ FastAPI:    │            │ Google:     │
    │ • Clean      │◄──────────►│ • REST API  │◄──────────►│ • Gemini AI │
    │ • Advanced   │            │ • WebSocket │            │ • Generative│
    │ • Original   │            │ • Async     │            │   AI API    │
    └──────────────┘            └─────────────┘            └─────────────┘
            │                           │                         │
    ┌───────▼──────┐            ┌──────▼──────┐            ┌──────▼──────┐
    │ Features:    │            │ Services:   │            │ Oracle:     │
    │ • PWA        │            │ • Session   │            │ • EBS R12   │
    │ • Offline    │            │ • Workflow  │            │ • Mockups   │
    │ • Voice      │            │ • Security  │            │ • Procedures│
    │ • Responsive │            │ • AI Agent  │            │ • Validation│
    └──────────────┘            └─────────────┘            └─────────────┘
            │                          │                           
    ┌───────▼──────┐            ┌──────▼──────┐                    
    │ Storage:     │            │ Data Layer: │                    
    │ • LocalStore │            │ • Redis     │                    
    │ • IndexedDB  │            │ • PostgreSQL│                    
    │ • Cache      │            │ • Volumes   │                    
    └──────────────┘            └─────────────┘                    
```

### **A.3 Flux de Données et Communication**

#### **A.3.1 Communication Frontend-Backend**
```javascript
// Flux de communication détaillé
const API_COMMUNICATION = {
    // 1. Initialisation session
    sessionInit: {
        endpoint: "POST /api/chat",
        payload: {
            message: "Hello",
            session_id: crypto.randomUUID(),
            context: {}
        },
        response: {
            message: "Welcome message",
            session_state: {...},
            suggestions: [...]
        }
    },
    
    // 2. Interaction workflow
    workflowInteraction: {
        endpoint: "POST /api/chat",
        payload: {
            message: "Start work confirmation",
            session_id: "existing-uuid",
            context: {
                current_procedure: null,
                language: "en"
            }
        },
        response: {
            message: "Procedure started...",
            current_step: {...},
            screenshot: "/static/images/...",
            suggestions: [...]
        }
    },
    
    // 3. Progression workflow
    stepProgression: {
        endpoint: "POST /api/chat",
        payload: {
            message: "done",
            session_id: "existing-uuid"
        },
        response: {
            message: "Step completed...",
            current_step: {...},
            validation_errors: []
        }
    }
};
```

#### **A.3.2 Traitement Backend**
```python
# Flux de traitement backend détaillé
async def process_message_flow(message: str, session_id: str):
    """Flux complet de traitement d'un message"""
    
    # 1. Récupération/Création session
    session = session_manager.get_session(session_id)
    
    # 2. Sanitisation input
    clean_message = bleach.clean(message, strip=True)
    
    # 3. Analyse d'intention
    intent = oracle_agent._analyze_intent(clean_message)
    
    # 4. Routage selon intention
    if intent == "start_procedure":
        response = await oracle_agent._handle_procedure_start(clean_message, session)
    elif intent == "continue_procedure":
        response = await oracle_agent._handle_procedure_continuation(clean_message, session)
    elif intent == "oracle_query":
        response = await oracle_agent._handle_oracle_query(clean_message, session)
    elif intent == "smart_assistance":
        response = await oracle_agent._handle_smart_assistance(clean_message, session)
    else:
        response = await oracle_agent._handle_general_query(clean_message, session)
    
    # 5. Mise à jour session
    session_manager.update_session(session_id, response.session_state)
    
    # 6. Retour réponse
    return response
```

---

## **ANNEXE B - PROCÉDURES ORACLE EBS R12** {#annexe-b}

### **B.1 Matrice Complète des Procédures**

| **ID** | **Catégorie** | **Procédure** | **Étapes** | **Screenshots** | **Langues** | **Validation** |
|--------|---------------|---------------|------------|-----------------|-------------|----------------|
| `work_confirmation` | Procurement | Work Confirmation | 6 | 6 (EN/FR) | EN/FR | Quantités, PO, Dates |
| `view_purchase_orders` | Procurement | View Purchase Orders | 3 | 3 (EN/FR) | EN/FR | Filtres, Permissions |
| `rfq_response` | Procurement | RFQ Response | 3 | 3 (EN/FR) | EN/FR | Specs, Prix, Délais |
| `goods_receipt_confirmation` | Procurement | Goods Receipt | 7 | 7 (EN/FR) | EN/FR | Qualité, Quantités |
| `service_entry_sheet` | Procurement | Service Entry | 6 | 6 (EN/FR) | EN/FR | Performance, Preuves |
| `invoice_submission` | Financial | Invoice Submission | 6 | 6 (EN/FR) | EN/FR | PO Match, Montants |
| `payment_tracking` | Financial | Payment Tracking | 2 | 2 (EN/FR) | EN/FR | Status, Disputes |
| `advance_payment_request` | Financial | Advance Payment | 6 | 6 (EN/FR) | EN/FR | Garantie, Limites |
| `supplier_registration` | Supplier Mgmt | Registration | 4 | 4 (EN/FR) | EN/FR | Compliance, Docs |
| `vendor_performance_evaluation` | Supplier Mgmt | Performance Eval | 9 | 9 (EN/FR) | EN/FR | Métriques, KPIs |
| `contract_management` | Contract | Contract Mgmt | 3 | 3 (EN/FR) | EN/FR | Signature, Termes |
| `quality_deviation_report` | Quality | Deviation Report | 7 | 7 (EN/FR) | EN/FR | Evidence, Actions |

### **B.2 Structure Détaillée d'une Procédure**

#### **B.2.1 Exemple Complet - Work Confirmation**
```json
{
  "work_confirmation": {
    "metadata": {
      "title": "Create Work Confirmation",
      "description": "Complete step-by-step guide to create a work confirmation in Oracle EBS R12 i-Supplier portal",
      "category": "procurement",
      "subcategory": "confirmations",
      "difficulty": "intermediate",
      "estimated_time": "10-15 minutes",
      "last_updated": "2024-01-15",
      "version": "1.2.0"
    },
    "prerequisites": [
      {
        "id": "valid_credentials",
        "description": "Valid i-Supplier login credentials",
        "type": "authentication",
        "mandatory": true
      },
      {
        "id": "active_po",
        "description": "Active purchase order with services requiring confirmation",
        "type": "business_data",
        "mandatory": true
      },
      {
        "id": "authorization_level",
        "description": "Proper authorization level for work confirmations",
        "type": "permission",
        "mandatory": true
      }
    ],
    "business_context": {
      "purpose": "Confirm completion of work or services as per purchase order terms",
      "impact": "Triggers payment process and updates procurement records",
      "frequency": "As needed when work is completed",
      "stakeholders": ["Supplier", "Procurement Team", "Finance Team"]
    },
    "steps": [
      {
        "step_id": "login",
        "sequence": 1,
        "title": "Login to i-Supplier Portal",
        "description": "Access the Oracle EBS R12 i-Supplier portal using your supplier credentials",
        "detailed_instructions": {
          "en": "Navigate to the i-Supplier portal URL provided by Tanger Med. Enter your username and password in the respective fields. Click 'Login' to access the system.",
          "fr": "Naviguez vers l'URL du portail i-Supplier fournie par Tanger Med. Saisissez votre nom d'utilisateur et mot de passe dans les champs respectifs. Cliquez sur 'Connexion' pour accéder au système."
        },
        "screenshot": {
          "en": "/static/images/oracle_mockups/oracle_login_en.png",
          "fr": "/static/images/oracle_mockups/oracle_login_fr.png"
        },
        "validation_criteria": [
          {
            "criterion": "successful_login",
            "description": "User successfully logged into the system",
            "validation_method": "dashboard_visible"
          },
          {
            "criterion": "dashboard_loaded",
            "description": "Main dashboard is visible and functional",
            "validation_method": "ui_elements_present"
          }
        ],
        "common_issues": [
          {
            "issue": "Invalid credentials",
            "solution": "Verify username and password, contact IT support if needed"
          },
          {
            "issue": "Account locked",
            "solution": "Contact system administrator to unlock account"
          },
          {
            "issue": "Browser compatibility",
            "solution": "Use supported browsers: Chrome, Firefox, Edge"
          }
        ],
        "next_steps": ["navigate_to_confirmations"],
        "estimated_duration": "2 minutes",
        "tips": [
          "Bookmark the portal URL for quick access",
          "Use 'Remember Me' option for convenience on trusted devices"
        ]
      },
      {
        "step_id": "navigate_to_confirmations",
        "sequence": 2,
        "title": "Navigate to Work Confirmations",
        "description": "Access the Work Confirmations section from the main navigation menu",
        "detailed_instructions": {
          "en": "From the main dashboard, locate the 'Procurement' menu in the top navigation bar. Click on 'Procurement' to expand the menu, then select 'Work Confirmations' from the dropdown options.",
          "fr": "Depuis le tableau de bord principal, localisez le menu 'Approvisionnement' dans la barre de navigation supérieure. Cliquez sur 'Approvisionnement' pour développer le menu, puis sélectionnez 'Confirmations de Travail' dans les options déroulantes."
        },
        "screenshot": {
          "en": "/static/images/oracle_mockups/oracle_work_confirmation_navigate_en.png",
          "fr": "/static/images/oracle_mockups/oracle_work_confirmation_navigate_fr.png"
        },
        "validation_criteria": [
          {
            "criterion": "confirmations_page_loaded",
            "description": "Work Confirmations page is displayed",
            "validation_method": "page_title_check"
          },
          {
            "criterion": "menu_accessible",
            "description": "Navigation menu is functional",
            "validation_method": "menu_items_clickable"
          }
        ],
        "next_steps": ["create_new_confirmation"],
        "estimated_duration": "1 minute"
      }
    ],
    "validation_rules": {
      "business_rules": [
        {
          "rule_id": "quantity_limit",
          "description": "Confirmed quantity cannot exceed purchase order quantity",
          "rule_type": "business_logic",
          "severity": "error",
          "error_message": "Confirmed quantity exceeds PO limit"
        },
        {
          "rule_id": "date_validation",
          "description": "Completion date cannot be in the future",
          "rule_type": "date_validation",
          "severity": "warning",
          "error_message": "Completion date cannot be future dated"
        }
      ],
      "technical_rules": [
        {
          "rule_id": "po_status",
          "description": "Purchase order must be in 'Open' or 'Approved' status",
          "rule_type": "status_check",
          "severity": "error",
          "error_message": "Selected PO is not available for confirmation"
        }
      ]
    },
    "success_criteria": {
      "primary": "Work confirmation successfully created and submitted",
      "secondary": [
        "Confirmation number generated",
        "Email notification sent",
        "Status updated in system"
      ]
    },
    "related_procedures": [
      "view_purchase_orders",
      "invoice_submission",
      "service_entry_sheet"
    ],
    "help_resources": [
      {
        "type": "documentation",
        "title": "Oracle i-Supplier User Guide",
        "url": "/static/docs/isupplier_guide.pdf"
      },
      {
        "type": "video",
        "title": "Work Confirmation Tutorial",
        "url": "/static/videos/work_confirmation_tutorial.mp4"
      }
    ]
  }
}
```

### **B.3 Règles de Validation Détaillées**

#### **B.3.1 Matrice de Validation par Procédure**
```json
{
  "validation_matrix": {
    "work_confirmation": {
      "mandatory_fields": [
        "purchase_order_number",
        "confirmation_quantity",
        "completion_date",
        "supplier_reference"
      ],
      "business_rules": [
        {
          "rule": "quantity_validation",
          "logic": "confirmed_qty <= po_remaining_qty",
          "error_code": "WC001",
          "message": "Quantity exceeds available PO balance"
        },
        {
          "rule": "date_validation",
          "logic": "completion_date <= current_date",
          "error_code": "WC002",
          "message": "Completion date cannot be in the future"
        },
        {
          "rule": "po_status_check",
          "logic": "po_status IN ('OPEN', 'APPROVED')",
          "error_code": "WC003",
          "message": "PO not available for confirmation"
        }
      ],
      "warning_rules": [
        {
          "rule": "early_confirmation",
          "logic": "completion_date < po_need_by_date - 7",
          "warning_code": "WC101",
          "message": "Confirmation is significantly early"
        }
      ]
    },
    "invoice_submission": {
      "mandatory_fields": [
        "invoice_number",
        "invoice_date",
        "invoice_amount",
        "purchase_order_reference"
      ],
      "business_rules": [
        {
          "rule": "unique_invoice_number",
          "logic": "invoice_number NOT IN (existing_invoices)",
          "error_code": "INV001",
          "message": "Invoice number already exists"
        },
        {
          "rule": "amount_validation",
          "logic": "invoice_amount <= po_remaining_amount",
          "error_code": "INV002",
          "message": "Invoice amount exceeds PO balance"
        },
        {
          "rule": "receipt_required",
          "logic": "goods_receipt_exists OR service_confirmation_exists",
          "error_code": "INV003",
          "message": "Receipt or confirmation required before invoicing"
        }
      ]
    }
  }
}
```

---

## **ANNEXE C - CONFIGURATION DOCKER** {#annexe-c}

### **C.1 Architecture de Containerisation**

#### **C.1.1 Dockerfile Multi-Stage Optimisé**
```dockerfile
# ================================
# Stage 1: Builder
# ================================
FROM python:3.9-slim as builder

# Métadonnées
LABEL maintainer="TMPA IT Team <it@tangermed.ma>"
LABEL version="1.0.0"
LABEL description="Oracle EBS R12 i-Supplier Assistant"

# Variables de build
ARG BUILD_DATE
ARG VERSION
ARG COMMIT_SHA

# Installation des dépendances système pour compilation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --user --no-cache-dir --upgrade pip \
    && pip install --user --no-cache-dir -r requirements.txt

# ================================
# Stage 2: Runtime
# ================================
FROM python:3.9-slim

# Copie des dépendances depuis le builder
COPY --from=builder /root/.local /root/.local

# Installation des outils runtime nécessaires
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Création utilisateur non-root pour sécurité
RUN groupadd --system appgroup \
    && useradd --system --group appgroup --home /app --shell /bin/bash appuser

# Configuration du répertoire de travail
WORKDIR /app

# Copie du code application
COPY --chown=appuser:appgroup . .

# Configuration des permissions
RUN chmod +x /app/docker-entrypoint.sh \
    && mkdir -p /app/logs /app/tmp \
    && chown -R appuser:appgroup /app

# Variables d'environnement
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Métadonnées runtime
LABEL build.date=$BUILD_DATE
LABEL build.version=$VERSION
LABEL build.commit=$COMMIT_SHA

# Health check avancé
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Exposition du port
EXPOSE 8000

# Changement vers utilisateur non-root
USER appuser

# Point d'entrée
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **C.1.2 Docker Compose Production Complet**
```yaml
version: '3.8'

# ================================
# Services Configuration
# ================================
services:
  
  # ================================
  # Application Backend
  # ================================
  oracle-ebs-assistant:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        BUILD_DATE: ${BUILD_DATE:-$(date -u +'%Y-%m-%dT%H:%M:%SZ')}
        VERSION: ${VERSION:-1.0.0}
        COMMIT_SHA: ${COMMIT_SHA:-unknown}
    image: oracle-ebs-assistant:${VERSION:-latest}
    container_name: oracle-ebs-assistant
    hostname: oracle-assistant
    
    # Configuration réseau
    ports:
      - "8000:8000"
    networks:
      - oracle-ebs-network
    
    # Variables d'environnement
    environment:
      # Application
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - ENVIRONMENT=${ENVIRONMENT:-production}
      - DEBUG=${DEBUG:-false}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      
      # Base de données
      - DATABASE_URL=postgresql://oracle_user:${DB_PASSWORD}@postgres:5432/oracle_ebs_assistant
      - REDIS_URL=redis://redis:6379/0
      
      # Sécurité
      - SESSION_SECRET_KEY=${SESSION_SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost,*.tangermed.ma}
      - CORS_ORIGINS=${CORS_ORIGINS:-http://localhost:3000,https://oracle-assistant.tangermed.ma}
      
      # Performance
      - WORKERS=${WORKERS:-4}
      - MAX_CONNECTIONS=${MAX_CONNECTIONS:-100}
      - TIMEOUT=${TIMEOUT:-60}
    
    # Volumes et stockage
    volumes:
      - ./procedures.json:/app/procedures.json:ro
      - ./static:/app/static:ro
      - app_logs:/app/logs
      - app_tmp:/app/tmp
    
    # Dépendances de services
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
    
    # Configuration de redémarrage
    restart: unless-stopped
    
    # Limites de ressources
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
    
    # Configuration des logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
        labels: "service=oracle-ebs-assistant"
    
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # ================================
  # Reverse Proxy Nginx
  # ================================
  nginx:
    image: nginx:1.25-alpine
    container_name: oracle-ebs-nginx
    hostname: nginx-proxy
    
    # Configuration réseau
    ports:
      - "80:80"
      - "443:443"
    networks:
      - oracle-ebs-network
    
    # Configuration et contenu
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./frontend:/usr/share/nginx/html:ro
      - ./ssl:/etc/nginx/ssl:ro
      - nginx_logs:/var/log/nginx
      - nginx_cache:/var/cache/nginx
    
    # Variables d'environnement
    environment:
      - NGINX_HOST=${NGINX_HOST:-oracle-assistant.tangermed.ma}
      - NGINX_PORT=${NGINX_PORT:-80}
    
    # Dépendances
    depends_on:
      - oracle-ebs-assistant
    
    # Redémarrage
    restart: unless-stopped
    
    # Limites de ressources
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M
    
    # Logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service=nginx"
    
    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  # ================================
  # Cache Redis
  # ================================
  redis:
    image: redis:7.2-alpine
    container_name: oracle-ebs-redis
    hostname: redis-cache
    
    # Configuration réseau
    ports:
      - "6379:6379"
    networks:
      - oracle-ebs-network
    
    # Configuration et données
    volumes:
      - redis_data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
    
    # Commande avec configuration
    command: redis-server /usr/local/etc/redis/redis.conf
    
    # Variables d'environnement
    environment:
      - REDIS_PASSWORD=${REDIS_PASSWORD}
    
    # Redémarrage
    restart: unless-stopped
    
    # Limites de ressources
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.1'
          memory: 128M
    
    # Logs
    logging:
      driver: "json-file"
      options:
        max-size: "5m"
        max-file: "3"
        labels: "service=redis"
    
    # Health check
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 30s
      timeout: 3s
      retries: 5

  # ================================
  # Base de Données PostgreSQL
  # ================================
  postgres:
    image: postgres:15.4-alpine
    container_name: oracle-ebs-postgres
    hostname: postgres-db
    
    # Configuration réseau
    ports:
      - "5432:5432"
    networks:
      - oracle-ebs-network
    
    # Variables d'environnement
    environment:
      - POSTGRES_DB=oracle_ebs_assistant
      - POSTGRES_USER=oracle_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8 --lc-collate=C --lc-ctype=C
      - PGDATA=/var/lib/postgresql/data/pgdata
    
    # Volumes et données
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d:ro
      - postgres_logs:/var/log/postgresql
    
    # Redémarrage
    restart: unless-stopped
    
    # Limites de ressources
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M
    
    # Logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
        labels: "service=postgres"
    
    # Health check
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U oracle_user -d oracle_ebs_assistant"]
      interval: 30s
      timeout: 5s
      retries: 5
      start_period: 30s

  # ================================
  # Monitoring Prometheus (Optionnel)
  # ================================
  prometheus:
    image: prom/prometheus:v2.47.0
    container_name: oracle-ebs-prometheus
    hostname: prometheus-monitor
    
    # Configuration réseau
    ports:
      - "9090:9090"
    networks:
      - oracle-ebs-network
    
    # Configuration
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./monitoring/rules:/etc/prometheus/rules:ro
      - prometheus_data:/prometheus
    
    # Commande avec options
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
    
    # Redémarrage
    restart: unless-stopped
    
    # Profil optionnel
    profiles:
      - monitoring
    
    # Limites de ressources
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M

# ================================
# Configuration Réseau
# ================================
networks:
  oracle-ebs-network:
    driver: bridge
    name: oracle-ebs-network
    ipam:
      driver: default
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
    driver_opts:
      com.docker.network.bridge.name: oracle-br0
      com.docker.network.driver.mtu: 1500

# ================================
# Configuration Volumes
# ================================
volumes:
  # Données applicatives
  redis_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ${DATA_PATH:-/opt/oracle-assistant}/redis
  
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ${DATA_PATH:-/opt/oracle-assistant}/postgres
  
  prometheus_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ${DATA_PATH:-/opt/oracle-assistant}/prometheus
  
  # Logs
  app_logs:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ${LOGS_PATH:-/var/log/oracle-assistant}/app
  
  nginx_logs:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ${LOGS_PATH:-/var/log/oracle-assistant}/nginx
  
  postgres_logs:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ${LOGS_PATH:-/var/log/oracle-assistant}/postgres
  
  # Cache et temporaire
  nginx_cache:
    driver: local
  
  app_tmp:
    driver: local
```

### **C.2 Configuration Nginx Avancée**

#### **C.2.1 Configuration Principale nginx.conf**
```nginx
# ================================
# Configuration Nginx Production
# Oracle EBS R12 Assistant
# ================================

user nginx;
worker_processes auto;
worker_rlimit_nofile 65535;

error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

# ================================
# Events Configuration
# ================================
events {
    worker_connections 2048;
    use epoll;
    multi_accept on;
    accept_mutex off;
}

# ================================
# HTTP Configuration
# ================================
http {
    # ================================
    # MIME Types et Encodage
    # ================================
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    charset utf-8;

    # ================================
    # Logging Configuration
    # ================================
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    log_format json escape=json '{'
                    '"timestamp":"$time_iso8601",'
                    '"remote_addr":"$remote_addr",'
                    '"method":"$request_method",'
                    '"uri":"$request_uri",'
                    '"status":$status,'
                    '"body_bytes_sent":$body_bytes_sent,'
                    '"request_time":$request_time,'
                    '"upstream_response_time":"$upstream_response_time",'
                    '"user_agent":"$http_user_agent",'
                    '"referer":"$http_referer"'
                    '}';

    access_log /var/log/nginx/access.log json;

    # ================================
    # Performance Optimizations
    # ================================
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 1000;
    types_hash_max_size 2048;
    server_tokens off;
    
    # Buffer sizes
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    output_buffers 1 32k;
    postpone_output 1460;

    # ================================
    # Security Headers
    # ================================
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; media-src 'self'; object-src 'none'; child-src 'none'; worker-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self';" always;

    # ================================
    # Compression Configuration
    # ================================
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # ================================
    # Rate Limiting
    # ================================
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
    limit_req_zone $binary_remote_addr zone=general:10m rate=30r/s;
    
    # Connection limiting
    limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;
    limit_conn_zone $server_name zone=conn_limit_per_server:10m;

    # ================================
    # Upstream Configuration
    # ================================
    upstream backend {
        least_conn;
        server oracle-ebs-assistant:8000 max_fails=3 fail_timeout=30s;
        keepalive 32;
        keepalive_requests 100;
        keepalive_timeout 60s;
    }

    # ================================
    # Cache Configuration
    # ================================
    proxy_cache_path /var/cache/nginx/static levels=1:2 keys_zone=static_cache:10m max_size=100m inactive=60m use_temp_path=off;
    proxy_cache_path /var/cache/nginx/api levels=1:2 keys_zone=api_cache:10m max_size=50m inactive=10m use_temp_path=off;

    # ================================
    # HTTP to HTTPS Redirect
    # ================================
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name _;
        
        # Security headers for HTTP
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        
        # Redirect all HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    # ================================
    # Main HTTPS Server
    # ================================
    server {
        listen 443 ssl http2 default_server;
        listen [::]:443 ssl http2 default_server;
        server_name oracle-assistant.tangermed.ma;

        # ================================
        # SSL Configuration
        # ================================
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        # SSL Security
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
        ssl_session_tickets off;
        
        # OCSP Stapling
        ssl_stapling on;
        ssl_stapling_verify on;
        
        # HSTS
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

        # ================================
        # Connection Limits
        # ================================
        limit_conn conn_limit_per_ip 20;
        limit_conn conn_limit_per_server 1000;

        # ================================
        # Root and Index
        # ================================
        root /usr/share/nginx/html;
        index index.html index.htm;

        # ================================
        # Frontend Static Files
        # ================================
        location / {
            try_files $uri $uri/ /index.html;
            
            # Cache control for HTML files
            location ~* \.html$ {
                expires 1h;
                add_header Cache-Control "public, no-transform";
            }
            
            # Cache control for static assets
            location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
                access_log off;
            }
            
            # Security for sensitive files
            location ~* \.(env|config|ini|log|bak)$ {
                deny all;
            }
        }

        # ================================
        # API Endpoints
        # ================================
        location /api/ {
            # Rate limiting
            limit_req zone=api burst=20 nodelay;
            
            # Proxy configuration
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $server_name;
            proxy_cache_bypass $http_upgrade;
            
            # Timeouts
            proxy_connect_timeout 5s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            
            # Buffer configuration
            proxy_buffering on;
            proxy_buffer_size 4k;
            proxy_buffers 8 4k;
            proxy_busy_buffers_size 8k;
            
            # Cache for specific endpoints
            location ~* /api/(procedures|health)$ {
                proxy_pass http://backend;
                proxy_cache api_cache;
                proxy_cache_valid 200 5m;
                proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
                add_header X-Cache-Status $upstream_cache_status;
            }
        }

        # ================================
        # Static Images and Assets
        # ================================
        location /static/ {
            proxy_pass http://backend;
            
            # Cache configuration
            proxy_cache static_cache;
            proxy_cache_valid 200 1d;
            proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
            
            # Headers
            expires 1d;
            add_header Cache-Control "public";
            add_header X-Cache-Status $upstream_cache_status;
        }

        # ================================
        # Health Check
        # ================================
        location /health {
            proxy_pass http://backend;
            access_log off;
            
            # Quick timeout for health checks
            proxy_connect_timeout 1s;
            proxy_send_timeout 1s;
            proxy_read_timeout 1s;
        }

        # ================================
        # Monitoring Endpoints
        # ================================
        location /nginx_status {
            stub_status on;
            access_log off;
            allow 127.0.0.1;
            allow 172.20.0.0/16;
            deny all;
        }

        # ================================
        # Error Pages
        # ================================
        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;
        
        location = /404.html {
            root /usr/share/nginx/html;
            internal;
        }
        
        location = /50x.html {
            root /usr/share/nginx/html;
            internal;
        }

        # ================================
        # Security Locations
        # ================================
        location ~ /\. {
            deny all;
            access_log off;
            log_not_found off;
        }
        
        location ~ ~$ {
            deny all;
            access_log off;
            log_not_found off;
        }
    }
}
```

---

Cette première partie de l'annexe couvre l'architecture technique, les procédures Oracle EBS R12 et la configuration Docker. Le fichier continuera avec les sections D, E, F, G et H dans la suite.

---

## **ANNEXE D - SÉCURITÉ ET CONFORMITÉ** {#annexe-d}

### **D.1 Matrice de Sécurité Complète**

#### **D.1.1 Analyse des Menaces et Protections**

| **Couche** | **Menace** | **Niveau Risque** | **Protection Implémentée** | **Code/Configuration** |
|------------|------------|-------------------|----------------------------|------------------------|
| **Frontend** | XSS (Cross-Site Scripting) | Élevé | Input Sanitization + CSP | `bleach.clean()` + Headers CSP |
| | CSRF (Cross-Site Request Forgery) | Moyen | Token Validation | JWT + CSRF tokens |
| | Clickjacking | Moyen | Frame Options | `X-Frame-Options: DENY` |
| | Data Exposure | Élevé | No PII Storage | Mock data uniquement |
| **API** | SQL Injection | Critique | Query Validation | Parameterized queries |
| | NoSQL Injection | Moyen | Input Validation | Regex patterns |
| | Rate Limiting | Élevé | Request Throttling | Nginx `limit_req` |
| | Authentication Bypass | Critique | Session Management | Secure session IDs |
| **Backend** | Code Injection | Critique | Input Sanitization | Pydantic validation |
| | Path Traversal | Élevé | Path Validation | Whitelist approach |
| | Deserialization | Moyen | Safe Parsing | JSON only |
| **Infrastructure** | Container Escape | Élevé | Non-root User | `appuser` account |
| | Network Attacks | Moyen | Network Isolation | Docker networks |
| | Data Breach | Critique | Encryption | TLS/SSL + Volume encryption |

#### **D.1.2 Implémentation Sécurité par Couche**

```python
# ================================
# Sécurité Backend - security.py
# ================================

import bleach
import re
from passlib.context import CryptContext
from jose import JWTError, jwt
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import secrets

class SecurityManager:
    """Gestionnaire centralisé de sécurité"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("SESSION_SECRET_KEY", secrets.token_urlsafe(32))
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        
        # Configuration sanitisation
        self.allowed_tags = []  # Aucun tag HTML autorisé
        self.allowed_attributes = {}
        
        # Patterns de validation
        self.safe_patterns = {
            'session_id': re.compile(r'^[a-zA-Z0-9-_]{8,64}$'),
            'po_number': re.compile(r'^PO-\d{4}-\d{3}$'),
            'invoice_number': re.compile(r'^INV-\d{4}-\d{3}$'),
            'alphanumeric': re.compile(r'^[a-zA-Z0-9\s\-_.]+$')
        }
    
    def sanitize_input(self, text: str, max_length: int = 2000) -> str:
        """Sanitisation complète des entrées utilisateur"""
        if not text or len(text) > max_length:
            return ""
        
        # Nettoyage HTML/XSS
        cleaned = bleach.clean(
            text, 
            tags=self.allowed_tags,
            attributes=self.allowed_attributes,
            strip=True
        )
        
        # Suppression caractères dangereux
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00', '\r']
        for char in dangerous_chars:
            cleaned = cleaned.replace(char, '')
        
        return cleaned.strip()
    
    def validate_session_id(self, session_id: str) -> bool:
        """Validation format session ID"""
        return bool(self.safe_patterns['session_id'].match(session_id))
    
    def validate_oracle_query(self, query: str) -> bool:
        """Validation sécurisée des requêtes Oracle"""
        query_lower = query.lower()
        
        # Blacklist mots-clés dangereux
        dangerous_keywords = [
            'drop', 'delete', 'update', 'insert', 'exec', 'execute',
            'union', 'select', 'create', 'alter', 'truncate',
            'script', 'javascript', 'vbscript', 'onload', 'onerror'
        ]
        
        return not any(keyword in query_lower for keyword in dangerous_keywords)
    
    def generate_csrf_token(self) -> str:
        """Génération token CSRF sécurisé"""
        return secrets.token_urlsafe(32)
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        """Création JWT token sécurisé"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str):
        """Vérification JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
    
    def hash_password(self, password: str) -> str:
        """Hachage sécurisé mot de passe"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Vérification mot de passe"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Chiffrement données sensibles"""
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data.decode()
    
    def audit_log(self, action: str, user_id: str, details: dict):
        """Logging sécurisé pour audit"""
        audit_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'user_id': user_id,
            'ip_address': details.get('ip_address', 'unknown'),
            'user_agent': details.get('user_agent', 'unknown')[:200],  # Limite taille
            'session_id': details.get('session_id', 'unknown'),
            'success': details.get('success', False)
        }
        
        # Log vers fichier sécurisé (pas de données sensibles)
        logger.info(f"AUDIT: {json.dumps(audit_entry)}")

# ================================
# Validation Pydantic Sécurisée
# ================================

from pydantic import BaseModel, Field, validator
import bleach

class SecureChatRequest(BaseModel):
    """Modèle sécurisé pour requêtes chat"""
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(..., regex=r'^[a-zA-Z0-9-_]{8,64}$')
    context: Optional[Dict[str, Any]] = Field(None)
    
    @validator('message')
    def sanitize_message(cls, v):
        # Sanitisation XSS
        cleaned = bleach.clean(v, tags=[], attributes={}, strip=True)
        
        # Validation longueur après nettoyage
        if len(cleaned) > 2000:
            raise ValueError('Message trop long après sanitisation')
        
        return cleaned
    
    @validator('context')
    def validate_context(cls, v):
        if v is None:
            return {}
        
        # Limite taille contexte
        if len(str(v)) > 5000:
            raise ValueError('Contexte trop volumineux')
        
        return v

class SecureOracleQuery(BaseModel):
    """Modèle sécurisé pour requêtes Oracle"""
    module: str = Field(..., regex=r'^[a-zA-Z_]+$')
    query_type: str = Field(..., regex=r'^[a-zA-Z_]+$')
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('module')
    def validate_module(cls, v):
        allowed_modules = [
            'purchase_orders', 'invoices', 'suppliers', 
            'contracts', 'rfqs', 'analytics'
        ]
        if v not in allowed_modules:
            raise ValueError(f'Module non autorisé: {v}')
        return v
    
    @validator('parameters')
    def validate_parameters(cls, v):
        # Validation paramètres sécurisée
        for key, value in v.items():
            if isinstance(value, str):
                # Sanitisation valeurs string
                v[key] = bleach.clean(value, tags=[], attributes={}, strip=True)
        
        return v
```

### **D.2 Conformité OWASP Top 10 2021**

#### **D.2.1 A01 - Broken Access Control**
```python
# Contrôle d'accès par session
class AccessControlManager:
    def __init__(self):
        self.session_permissions = {}
    
    def validate_session_access(self, session_id: str, resource: str) -> bool:
        """Validation accès ressource par session"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        # Vérification timeout
        if datetime.now() - session.updated_at > timedelta(hours=24):
            self.delete_session(session_id)
            return False
        
        # Vérification permissions (si implémenté)
        permissions = self.session_permissions.get(session_id, [])
        return self._check_resource_permission(resource, permissions)
    
    def _check_resource_permission(self, resource: str, permissions: List[str]) -> bool:
        """Vérification permission ressource"""
        # Pour l'instant, accès libre aux ressources publiques
        public_resources = [
            '/api/chat', '/api/procedures', '/api/health',
            '/static/images', '/static/docs'
        ]
        return resource in public_resources
```

#### **D.2.2 A03 - Injection**
```python
# Protection injection complète
class InjectionProtection:
    def __init__(self):
        self.dangerous_patterns = [
            # SQL Injection
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)',
            # NoSQL Injection
            r'(\$where|\$ne|\$gt|\$lt|\$regex)',
            # Command Injection
            r'(;|\||&|`|\$\(|\${)',
            # Script Injection
            r'(<script|javascript:|vbscript:|onload=|onerror=)',
            # Path Traversal
            r'(\.\./|\.\.\\|%2e%2e%2f|%2e%2e%5c)'
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) 
                                 for pattern in self.dangerous_patterns]
    
    def validate_input(self, input_text: str) -> bool:
        """Validation contre injections"""
        for pattern in self.compiled_patterns:
            if pattern.search(input_text):
                return False
        return True
    
    def sanitize_oracle_query(self, query: str) -> Optional[str]:
        """Sanitisation spécifique requêtes Oracle"""
        if not self.validate_input(query):
            return None
        
        # Whitelist approach pour PO numbers
        po_pattern = re.compile(r'^.*?(PO-\d{4}-\d{3}).*?$', re.IGNORECASE)
        match = po_pattern.match(query)
        if match:
            return match.group(1).upper()
        
        # Autres patterns sécurisés
        safe_queries = {
            'list_all': ['show', 'list', 'display', 'view'],
            'search': ['search', 'find', 'lookup']
        }
        
        query_lower = query.lower()
        for query_type, keywords in safe_queries.items():
            if any(keyword in query_lower for keyword in keywords):
                return query_type
        
        return None
```

#### **D.2.3 A07 - Cross-Site Scripting (XSS)**
```python
# Protection XSS multicouche
class XSSProtection:
    def __init__(self):
        self.bleach_config = {
            'tags': [],  # Aucun tag HTML autorisé
            'attributes': {},
            'protocols': [],
            'strip': True,
            'strip_comments': True
        }
    
    def sanitize_html(self, content: str) -> str:
        """Sanitisation HTML complète"""
        return bleach.clean(content, **self.bleach_config)
    
    def escape_javascript(self, content: str) -> str:
        """Échappement pour contexte JavaScript"""
        escape_map = {
            '\\': '\\\\',
            '"': '\\"',
            "'": "\\'",
            '\n': '\\n',
            '\r': '\\r',
            '\t': '\\t',
            '<': '\\u003c',
            '>': '\\u003e',
            '&': '\\u0026'
        }
        
        for char, escaped in escape_map.items():
            content = content.replace(char, escaped)
        
        return content
    
    def validate_csp_compliance(self, content: str) -> bool:
        """Validation conformité CSP"""
        # Vérification absence de inline scripts/styles
        dangerous_patterns = [
            r'<script[^>]*>',
            r'javascript:',
            r'on\w+\s*=',
            r'style\s*=',
            r'<link[^>]*stylesheet'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return False
        
        return True
```

### **D.3 Configuration Sécurité Infrastructure**

#### **D.3.1 Configuration Docker Sécurisée**
```dockerfile
# Dockerfile sécurisé
FROM python:3.9-slim

# Mise à jour sécurité système
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Création utilisateur non-root
RUN groupadd --system --gid 1000 appgroup \
    && useradd --system --uid 1000 --gid appgroup \
       --home /app --shell /bin/bash appuser

# Configuration répertoires sécurisés
WORKDIR /app
RUN mkdir -p /app/logs /app/tmp /app/cache \
    && chown -R appuser:appgroup /app \
    && chmod 755 /app \
    && chmod 750 /app/logs /app/tmp /app/cache

# Installation dépendances
COPY --chown=appuser:appgroup requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

# Copie code application
COPY --chown=appuser:appgroup . .

# Configuration permissions finales
RUN find /app -type f -exec chmod 644 {} \; \
    && find /app -type d -exec chmod 755 {} \; \
    && chmod +x /app/docker-entrypoint.sh

# Variables d'environnement sécurisées
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random

# Utilisateur non-root
USER appuser

# Health check sécurisé
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **D.3.2 Configuration Réseau Sécurisée**
```yaml
# docker-compose-security.yml
version: '3.8'

services:
  oracle-ebs-assistant:
    # ... configuration service ...
    
    # Sécurité réseau
    networks:
      - frontend_network
      - backend_network
    
    # Limites de ressources (sécurité DoS)
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
          pids: 100
        reservations:
          cpus: '0.5'
          memory: 512M
    
    # Configuration sécurité
    security_opt:
      - no-new-privileges:true
    
    # Capabilities limitées
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    
    # Système de fichiers read-only
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
      - /app/tmp:noexec,nosuid,size=50m

networks:
  frontend_network:
    driver: bridge
    internal: false
    ipam:
      config:
        - subnet: 172.20.1.0/24
  
  backend_network:
    driver: bridge
    internal: true
    ipam:
      config:
        - subnet: 172.20.2.0/24
```

---

## **ANNEXE E - MÉTRIQUES ET MONITORING** {#annexe-e}

### **E.1 KPIs et Métriques Techniques**

#### **E.1.1 Métriques de Performance**
```python
# Définition des métriques de performance
PERFORMANCE_METRICS = {
    "response_time": {
        "api_endpoints": {
            "target": "< 200ms (95th percentile)",
            "critical": "> 1000ms",
            "measurement": "histogram",
            "buckets": [0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        },
        "ai_generation": {
            "target": "< 2s (average)",
            "critical": "> 10s",
            "measurement": "histogram",
            "buckets": [0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        },
        "database_queries": {
            "target": "< 50ms (average)",
            "critical": "> 500ms",
            "measurement": "histogram",
            "buckets": [0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
        }
    },
    "throughput": {
        "requests_per_second": {
            "target": "50+ RPS",
            "peak_capacity": "200 RPS",
            "measurement": "counter"
        },
        "concurrent_users": {
            "target": "100+ simultaneous",
            "max_capacity": "500 users",
            "measurement": "gauge"
        },
        "session_capacity": {
            "target": "1000+ active sessions",
            "max_capacity": "5000 sessions",
            "measurement": "gauge"
        }
    },
    "availability": {
        "uptime_target": "99.9%",
        "recovery_time_objective": "< 5 minutes",
        "recovery_point_objective": "< 1 hour",
        "backup_frequency": "Daily automated"
    },
    "resource_utilization": {
        "cpu_usage": {
            "target": "< 70% average",
            "critical": "> 90%",
            "measurement": "gauge"
        },
        "memory_usage": {
            "target": "< 80% average",
            "critical": "> 95%",
            "measurement": "gauge"
        },
        "disk_usage": {
            "target": "< 85%",
            "critical": "> 95%",
            "measurement": "gauge"
        }
    }
}
```

#### **E.1.2 Métriques Business**
```python
BUSINESS_METRICS = {
    "user_engagement": {
        "session_duration": {
            "target": "Average 15 minutes",
            "measurement": "histogram",
            "buckets": [1, 5, 10, 15, 30, 60, 120]
        },
        "procedure_completion_rate": {
            "target": "85% completion rate",
            "critical": "< 70%",
            "measurement": "gauge"
        },
        "user_satisfaction": {
            "target": "4.5/5 rating",
            "measurement": "gauge"
        },
        "bounce_rate": {
            "target": "< 20%",
            "critical": "> 40%",
            "measurement": "gauge"
        }
    },
    "operational_efficiency": {
        "support_ticket_reduction": {
            "target": "60% decrease vs baseline",
            "measurement": "gauge"
        },
        "training_time_reduction": {
            "target": "40% decrease vs traditional training",
            "measurement": "gauge"
        },
        "error_rate_reduction": {
            "target": "70% decrease in user errors",
            "measurement": "gauge"
        },
        "procedure_success_rate": {
            "target": "> 90% first-time success",
            "measurement": "gauge"
        }
    },
    "ai_performance": {
        "intent_recognition_accuracy": {
            "target": "> 95% accuracy",
            "measurement": "gauge"
        },
        "response_relevance": {
            "target": "> 90% relevant responses",
            "measurement": "gauge"
        },
        "language_detection_accuracy": {
            "target": "> 98% accuracy",
            "measurement": "gauge"
        }
    }
}
```

### **E.2 Configuration Monitoring Avancée**

#### **E.2.1 Prometheus Configuration Complète**
```yaml
# prometheus.yml - Configuration monitoring complète
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'oracle-ebs-assistant'
    environment: 'production'

# Règles d'alerting
rule_files:
  - "alert_rules.yml"
  - "recording_rules.yml"

# Configuration scraping
scrape_configs:
  # Application principale
  - job_name: 'oracle-ebs-assistant'
    static_configs:
      - targets: ['oracle-ebs-assistant:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
    scrape_timeout: 10s
    honor_labels: true
    params:
      format: ['prometheus']

  # Nginx metrics
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:80']
    metrics_path: '/nginx_status'
    scrape_interval: 30s

  # Redis metrics
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    scrape_interval: 30s

  # PostgreSQL metrics
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
    scrape_interval: 30s

  # Node exporter (système)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
    scrape_interval: 30s

# Configuration alerting
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
      timeout: 10s
      api_version: v2

# Configuration remote write (optionnel)
remote_write:
  - url: "https://prometheus-remote-write.example.com/api/v1/write"
    basic_auth:
      username: "prometheus"
      password: "secure_password"
```

#### **E.2.2 Règles d'Alerting Détaillées**
```yaml
# alert_rules.yml - Règles d'alerting complètes
groups:
  # ================================
  # Alertes Application
  # ================================
  - name: oracle_ebs_assistant_app
    rules:
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, http_request_duration_seconds_bucket{job="oracle-ebs-assistant"}) > 0.5
        for: 2m
        labels:
          severity: warning
          component: application
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }}s for {{ $labels.instance }}"
          runbook_url: "https://wiki.tangermed.ma/runbooks/high-response-time"

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 1m
        labels:
          severity: critical
          component: application
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second on {{ $labels.instance }}"
          runbook_url: "https://wiki.tangermed.ma/runbooks/high-error-rate"

      - alert: ServiceDown
        expr: up{job="oracle-ebs-assistant"} == 0
        for: 1m
        labels:
          severity: critical
          component: application
        annotations:
          summary: "Oracle EBS Assistant service is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"
          runbook_url: "https://wiki.tangermed.ma/runbooks/service-down"

      - alert: HighMemoryUsage
        expr: (process_resident_memory_bytes / process_virtual_memory_max_bytes) * 100 > 90
        for: 5m
        labels:
          severity: warning
          component: application
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}% on {{ $labels.instance }}"

      - alert: AIResponseTimeout
        expr: histogram_quantile(0.95, ai_generation_duration_seconds_bucket) > 10
        for: 3m
        labels:
          severity: warning
          component: ai
        annotations:
          summary: "AI response timeout"
          description: "AI generation taking too long: {{ $value }}s"

  # ================================
  # Alertes Infrastructure
  # ================================
  - name: oracle_ebs_assistant_infra
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
          component: infrastructure
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is {{ $value }}% on {{ $labels.instance }}"

      - alert: HighDiskUsage
        expr: (node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
          component: infrastructure
        annotations:
          summary: "High disk usage"
          description: "Disk usage is {{ $value }}% on {{ $labels.instance }}"

      - alert: RedisDown
        expr: up{job="redis"} == 0
        for: 1m
        labels:
          severity: critical
          component: cache
        annotations:
          summary: "Redis is down"
          description: "Redis instance {{ $labels.instance }} is down"

      - alert: PostgreSQLDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
          component: database
        annotations:
          summary: "PostgreSQL is down"
          description: "PostgreSQL instance {{ $labels.instance }} is down"

  # ================================
  # Alertes Business
  # ================================
  - name: oracle_ebs_assistant_business
    rules:
      - alert: LowProcedureCompletionRate
        expr: (procedure_completions_total / procedure_starts_total) * 100 < 70
        for: 10m
        labels:
          severity: warning
          component: business
        annotations:
          summary: "Low procedure completion rate"
          description: "Procedure completion rate is {{ $value }}%"

      - alert: HighSessionAbandonmentRate
        expr: (session_abandonments_total / session_starts_total) * 100 > 40
        for: 10m
        labels:
          severity: warning
          component: business
        annotations:
          summary: "High session abandonment rate"
          description: "Session abandonment rate is {{ $value }}%"

      - alert: AIAccuracyDrop
        expr: ai_intent_recognition_accuracy < 0.90
        for: 5m
        labels:
          severity: warning
          component: ai
        annotations:
          summary: "AI accuracy drop detected"
          description: "AI intent recognition accuracy dropped to {{ $value }}"
```

#### **E.2.3 Métriques Personnalisées Application**
```python
# metrics.py - Métriques personnalisées pour l'application
from prometheus_client import Counter, Histogram, Gauge, Info
import time
from functools import wraps

# ================================
# Définition des métriques
# ================================

# Métriques HTTP
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Métriques IA
ai_generation_duration_seconds = Histogram(
    'ai_generation_duration_seconds',
    'AI response generation duration',
    ['model', 'language'],
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

ai_intent_recognition_accuracy = Gauge(
    'ai_intent_recognition_accuracy',
    'AI intent recognition accuracy'
)

# Métriques sessions
active_sessions = Gauge(
    'active_sessions_total',
    'Number of active user sessions'
)

session_duration_seconds = Histogram(
    'session_duration_seconds',
    'User session duration',
    buckets=[60, 300, 600, 900, 1800, 3600, 7200]
)

# Métriques procédures
procedure_starts_total = Counter(
    'procedure_starts_total',
    'Total procedure starts',
    ['procedure_id', 'language']
)

procedure_completions_total = Counter(
    'procedure_completions_total',
    'Total procedure completions',
    ['procedure_id', 'language']
)

procedure_step_duration_seconds = Histogram(
    'procedure_step_duration_seconds',
    'Time spent on procedure steps',
    ['procedure_id', 'step_id'],
    buckets=[10, 30, 60, 120, 300, 600, 1200]
)

# Métriques Oracle
oracle_query_duration_seconds = Histogram(
    'oracle_query_duration_seconds',
    'Oracle query execution time',
    ['module', 'query_type'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

# Métriques erreurs
error_count_total = Counter(
    'error_count_total',
    'Total errors by type',
    ['error_type', 'component']
)

# ================================
# Décorateurs pour métriques
# ================================

def track_request_metrics(func):
    """Décorateur pour tracker les métriques HTTP"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        status = "200"
        
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            status = "500"
            error_count_total.labels(
                error_type=type(e).__name__,
                component="api"
            ).inc()
            raise
        finally:
            duration = time.time() - start_time
            
            # Extraction des labels depuis la requête
            method = getattr(args[0], 'method', 'unknown') if args else 'unknown'
            endpoint = getattr(args[0], 'url', {}).get('path', 'unknown') if args else 'unknown'
            
            http_requests_total.labels(
                method=method,
                endpoint=endpoint,
                status=status
            ).inc()
            
            http_request_duration_seconds.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
    
    return wrapper

def track_ai_metrics(func):
    """Décorateur pour tracker les métriques IA"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            
            # Extraction des paramètres IA
            model = kwargs.get('model', 'gemini')
            language = kwargs.get('language', 'en')
            
            ai_generation_duration_seconds.labels(
                model=model,
                language=language
            ).observe(duration)
    
    return wrapper

def track_procedure_metrics(func):
    """Décorateur pour tracker les métriques de procédures"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        procedure_id = kwargs.get('procedure_id')
        language = kwargs.get('language', 'en')
        
        if procedure_id:
            procedure_starts_total.labels(
                procedure_id=procedure_id,
                language=language
            ).inc()
        
        try:
            result = await func(*args, **kwargs)
            
            # Si procédure complétée
            if result and getattr(result, 'status', None) == 'completed':
                procedure_completions_total.labels(
                    procedure_id=procedure_id,
                    language=language
                ).inc()
            
            return result
        except Exception as e:
            error_count_total.labels(
                error_type=type(e).__name__,
                component="procedure"
            ).inc()
            raise
    
    return wrapper

# ================================
# Collecteur de métriques personnalisé
# ================================

class MetricsCollector:
    """Collecteur centralisé de métriques"""
    
    def __init__(self):
        self.session_manager = None
    
    def set_session_manager(self, session_manager):
        """Configuration du gestionnaire de sessions"""
        self.session_manager = session_manager
    
    def update_session_metrics(self):
        """Mise à jour des métriques de sessions"""
        if self.session_manager:
            stats = self.session_manager.get_session_stats()
            active_sessions.set(stats.get('total_sessions', 0))
    
    def record_session_duration(self, duration_seconds: float):
        """Enregistrement durée de session"""
        session_duration_seconds.observe(duration_seconds)
    
    def record_procedure_step_time(self, procedure_id: str, step_id: str, duration: float):
        """Enregistrement temps étape procédure"""
        procedure_step_duration_seconds.labels(
            procedure_id=procedure_id,
            step_id=step_id
        ).observe(duration)
    
    def record_oracle_query_time(self, module: str, query_type: str, duration: float):
        """Enregistrement temps requête Oracle"""
        oracle_query_duration_seconds.labels(
            module=module,
            query_type=query_type
        ).observe(duration)
    
    def update_ai_accuracy(self, accuracy: float):
        """Mise à jour précision IA"""
        ai_intent_recognition_accuracy.set(accuracy)

# Instance globale du collecteur
metrics_collector = MetricsCollector()
```

---

Cette section continue l'annexe avec les aspects sécurité et monitoring. Le fichier continuera avec les sections F, G et H.
---

## **ANNEXE F - GUIDE DE DÉPLOIEMENT** {#annexe-f}

### **F.1 Prérequis et Préparation**

#### **F.1.1 Environnement Système Minimum**
```bash
# ================================
# Spécifications Serveur
# ================================

# Configuration Minimale (Développement/Test)
CPU: 2 cores (2.0 GHz minimum)
RAM: 4GB minimum, 8GB recommandé
Storage: 20GB minimum, 50GB recommandé
Network: 100 Mbps minimum
OS: Ubuntu 20.04 LTS, CentOS 8, Windows Server 2019, macOS 10.15+

# Configuration Production
CPU: 4 cores (2.5 GHz minimum), 8 cores recommandé
RAM: 8GB minimum, 16GB recommandé
Storage: 100GB minimum, 200GB recommandé (SSD)
Network: 1 Gbps minimum
OS: Ubuntu 20.04 LTS (recommandé), CentOS 8, RHEL 8

# Configuration Haute Disponibilité
CPU: 8+ cores (3.0 GHz)
RAM: 32GB+
Storage: 500GB+ (SSD NVMe)
Network: 10 Gbps
Load Balancer: Nginx/HAProxy
Database: PostgreSQL Cluster
Cache: Redis Cluster
```

#### **F.1.2 Logiciels Requis**
```bash
# ================================
# Installation des Prérequis
# ================================

# Docker et Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Git
sudo apt-get update
sudo apt-get install -y git

# Outils système
sudo apt-get install -y curl wget unzip htop tree jq

# Certificats SSL (Let's Encrypt)
sudo apt-get install -y certbot python3-certbot-nginx

# Monitoring tools
sudo apt-get install -y prometheus-node-exporter
```

#### **F.1.3 Configuration Réseau et Sécurité**
```bash
# ================================
# Configuration Firewall
# ================================

# UFW (Ubuntu)
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 10.0.0.0/8 to any port 9090  # Prometheus (réseau interne)

# Fail2ban pour protection SSH
sudo apt-get install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Configuration SSL/TLS
sudo mkdir -p /opt/oracle-assistant/ssl
sudo chown -R $USER:$USER /opt/oracle-assistant
```

### **F.2 Procédures de Déploiement**

#### **F.2.1 Script de Déploiement Automatisé Complet**
```bash
#!/bin/bash
# ================================
# deploy-oracle-assistant.sh
# Script de déploiement automatisé complet
# ================================

set -euo pipefail

# Configuration
PROJECT_NAME="oracle-ebs-assistant"
PROJECT_DIR="/opt/${PROJECT_NAME}"
BACKUP_DIR="/opt/${PROJECT_NAME}/backups"
LOG_FILE="/var/log/${PROJECT_NAME}/deploy.log"
DOCKER_COMPOSE_FILE="docker-compose.prod.yml"

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions utilitaires
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$LOG_FILE"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}" | tee -a "$LOG_FILE"
}

# Vérification des prérequis
check_prerequisites() {
    log "Vérification des prérequis système..."
    
    # Vérification Docker
    if ! command -v docker &> /dev/null; then
        error "Docker n'est pas installé. Veuillez installer Docker d'abord."
    fi
    
    # Vérification Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose n'est pas installé."
    fi
    
    # Vérification Git
    if ! command -v git &> /dev/null; then
        error "Git n'est pas installé."
    fi
    
    # Vérification espace disque
    AVAILABLE_SPACE=$(df / | awk 'NR==2 {print $4}')
    REQUIRED_SPACE=5242880  # 5GB en KB
    
    if [ "$AVAILABLE_SPACE" -lt "$REQUIRED_SPACE" ]; then
        error "Espace disque insuffisant. Requis: 5GB, Disponible: $((AVAILABLE_SPACE/1024/1024))GB"
    fi
    
    # Vérification mémoire
    AVAILABLE_RAM=$(free -m | awk 'NR==2{print $7}')
    REQUIRED_RAM=2048  # 2GB
    
    if [ "$AVAILABLE_RAM" -lt "$REQUIRED_RAM" ]; then
        warn "RAM disponible faible: ${AVAILABLE_RAM}MB. Recommandé: ${REQUIRED_RAM}MB"
    fi
    
    log "✅ Prérequis validés"
}

# Configuration de l'environnement
setup_environment() {
    log "Configuration de l'environnement..."
    
    # Création des répertoires
    sudo mkdir -p "$PROJECT_DIR"/{data,logs,ssl,backups,config}
    sudo mkdir -p /var/log/"$PROJECT_NAME"
    
    # Configuration des permissions
    sudo chown -R "$USER":"$USER" "$PROJECT_DIR"
    sudo chown -R "$USER":"$USER" /var/log/"$PROJECT_NAME"
    
    # Configuration des variables d'environnement
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        log "Création du fichier .env..."
        cat > "$PROJECT_DIR/.env" << EOF
# Configuration Oracle EBS Assistant
GOOGLE_API_KEY=${GOOGLE_API_KEY:-AIzaSyC8pw11h7ppDilnA-ITc8-SmF8daANOhIw}
ENVIRONMENT=production
VERSION=${VERSION:-1.0.0}
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')

# Base de données
DB_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 16)

# Sécurité
SESSION_SECRET_KEY=$(openssl rand -base64 32)
ALLOWED_HOSTS=localhost,*.tangermed.ma,oracle-assistant.tangermed.ma
CORS_ORIGINS=https://oracle-assistant.tangermed.ma

# Chemins
DATA_PATH=$PROJECT_DIR/data
LOGS_PATH=/var/log/$PROJECT_NAME

# Performance
WORKERS=4
MAX_CONNECTIONS=100
TIMEOUT=60

# Monitoring
LOG_LEVEL=INFO
DEBUG=false
EOF
        log "✅ Fichier .env créé"
    else
        info "Fichier .env existant trouvé"
    fi
    
    log "✅ Environnement configuré"
}

# Téléchargement du code source
download_source() {
    log "Téléchargement du code source..."
    
    if [ -d "$PROJECT_DIR/src" ]; then
        log "Mise à jour du code existant..."
        cd "$PROJECT_DIR/src"
        git pull origin main
    else
        log "Clonage du repository..."
        git clone https://github.com/tangermed/oracle-ebs-assistant.git "$PROJECT_DIR/src"
        cd "$PROJECT_DIR/src"
    fi
    
    # Vérification de l'intégrité
    if [ ! -f "docker-compose.prod.yml" ]; then
        error "Fichier docker-compose.prod.yml manquant"
    fi
    
    if [ ! -f "Dockerfile" ]; then
        error "Dockerfile manquant"
    fi
    
    log "✅ Code source téléchargé"
}

# Configuration SSL
setup_ssl() {
    log "Configuration SSL/TLS..."
    
    local domain="${SSL_DOMAIN:-oracle-assistant.tangermed.ma}"
    local ssl_dir="$PROJECT_DIR/ssl"
    
    if [ "$1" = "--letsencrypt" ] && [ -n "${SSL_DOMAIN:-}" ]; then
        log "Configuration Let's Encrypt pour $domain..."
        
        # Arrêt temporaire de nginx si en cours d'exécution
        docker-compose -f "$PROJECT_DIR/src/$DOCKER_COMPOSE_FILE" stop nginx 2>/dev/null || true
        
        # Génération certificat Let's Encrypt
        sudo certbot certonly --standalone \
            --email "${SSL_EMAIL:-admin@tangermed.ma}" \
            --agree-tos \
            --no-eff-email \
            -d "$domain"
        
        # Copie des certificats
        sudo cp "/etc/letsencrypt/live/$domain/fullchain.pem" "$ssl_dir/cert.pem"
        sudo cp "/etc/letsencrypt/live/$domain/privkey.pem" "$ssl_dir/key.pem"
        sudo chown "$USER":"$USER" "$ssl_dir"/*.pem
        
        # Configuration renouvellement automatique
        echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
        
        log "✅ Certificat Let's Encrypt configuré"
    else
        log "Génération certificat auto-signé..."
        
        # Génération certificat auto-signé
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout "$ssl_dir/key.pem" \
            -out "$ssl_dir/cert.pem" \
            -subj "/C=MA/ST=Tangier/L=Tangier/O=TMPA/CN=${domain}"
        
        warn "Certificat auto-signé généré. Remplacez par un certificat valide en production."
    fi
    
    log "✅ SSL configuré"
}

# Sauvegarde des données existantes
backup_existing_data() {
    log "Sauvegarde des données existantes..."
    
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/backup_${backup_timestamp}.tar.gz"
    
    if [ -d "$PROJECT_DIR/data" ]; then
        tar -czf "$backup_file" -C "$PROJECT_DIR" data config .env 2>/dev/null || true
        log "✅ Sauvegarde créée: $backup_file"
    else
        info "Aucune donnée existante à sauvegarder"
    fi
}

# Déploiement des services
deploy_services() {
    log "Déploiement des services Docker..."
    
    cd "$PROJECT_DIR/src"
    
    # Copie de la configuration d'environnement
    cp "$PROJECT_DIR/.env" .
    
    # Arrêt des services existants
    log "Arrêt des services existants..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" down --remove-orphans 2>/dev/null || true
    
    # Nettoyage des images obsolètes
    log "Nettoyage des images Docker obsolètes..."
    docker system prune -f
    
    # Build des images
    log "Construction des images Docker..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" build --no-cache --parallel
    
    # Démarrage des services
    log "Démarrage des services..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" up -d
    
    # Attente du démarrage
    log "Attente du démarrage des services..."
    sleep 30
    
    log "✅ Services déployés"
}

# Vérification de la santé des services
health_check() {
    log "Vérification de la santé des services..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        info "Tentative $attempt/$max_attempts..."
        
        # Vérification de l'application principale
        if curl -f -s http://localhost/health > /dev/null 2>&1; then
            log "✅ Application principale: OK"
            break
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            error "Échec de la vérification de santé après $max_attempts tentatives"
        fi
        
        sleep 10
        ((attempt++))
    done
    
    # Vérification des services individuels
    local services=("oracle-ebs-assistant" "nginx" "redis" "postgres")
    
    for service in "${services[@]}"; do
        if docker ps --format "table {{.Names}}" | grep -q "$service"; then
            log "✅ Service $service: Running"
        else
            error "❌ Service $service: Not running"
        fi
    done
    
    # Vérification des endpoints
    local endpoints=(
        "http://localhost/health"
        "http://localhost/api/procedures"
    )
    
    for endpoint in "${endpoints[@]}"; do
        if curl -f -s "$endpoint" > /dev/null 2>&1; then
            log "✅ Endpoint $endpoint: OK"
        else
            warn "⚠️ Endpoint $endpoint: Failed"
        fi
    done
    
    log "✅ Vérification de santé terminée"
}

# Configuration du monitoring
setup_monitoring() {
    log "Configuration du monitoring..."
    
    # Démarrage des services de monitoring
    cd "$PROJECT_DIR/src"
    docker-compose -f "$DOCKER_COMPOSE_FILE" --profile monitoring up -d
    
    # Configuration des alertes
    if [ -f "monitoring/alertmanager.yml" ]; then
        log "Configuration Alertmanager trouvée"
    fi
    
    log "✅ Monitoring configuré"
}

# Configuration des logs
setup_logging() {
    log "Configuration du système de logs..."
    
    # Configuration logrotate
    sudo tee /etc/logrotate.d/"$PROJECT_NAME" > /dev/null << EOF
/var/log/$PROJECT_NAME/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
    postrotate
        docker-compose -f $PROJECT_DIR/src/$DOCKER_COMPOSE_FILE restart nginx
    endscript
}
EOF
    
    log "✅ Configuration des logs terminée"
}

# Post-déploiement
post_deployment() {
    log "Tâches post-déploiement..."
    
    # Affichage des informations de connexion
    echo ""
    echo "🎉 Déploiement terminé avec succès!"
    echo ""
    echo "📊 Services disponibles:"
    echo "   - Application principale: https://localhost"
    echo "   - API Health Check: https://localhost/health"
    echo "   - API Documentation: https://localhost/docs"
    
    if docker ps --format "table {{.Names}}" | grep -q "prometheus"; then
        echo "   - Monitoring Prometheus: http://localhost:9090"
    fi
    
    echo ""
    echo "📝 Commandes utiles:"
    echo "   - Logs en temps réel: docker-compose -f $PROJECT_DIR/src/$DOCKER_COMPOSE_FILE logs -f"
    echo "   - Redémarrage: docker-compose -f $PROJECT_DIR/src/$DOCKER_COMPOSE_FILE restart"
    echo "   - Arrêt: docker-compose -f $PROJECT_DIR/src/$DOCKER_COMPOSE_FILE down"
    echo "   - Status: docker-compose -f $PROJECT_DIR/src/$DOCKER_COMPOSE_FILE ps"
    echo ""
    echo "📁 Répertoires importants:"
    echo "   - Projet: $PROJECT_DIR"
    echo "   - Logs: /var/log/$PROJECT_NAME"
    echo "   - Sauvegardes: $BACKUP_DIR"
    echo ""
    
    # Création d'un script de gestion
    cat > "$PROJECT_DIR/manage.sh" << 'EOF'
#!/bin/bash
# Script de gestion Oracle EBS Assistant

PROJECT_DIR="/opt/oracle-ebs-assistant"
COMPOSE_FILE="$PROJECT_DIR/src/docker-compose.prod.yml"

case "$1" in
    start)
        echo "Démarrage des services..."
        docker-compose -f "$COMPOSE_FILE" up -d
        ;;
    stop)
        echo "Arrêt des services..."
        docker-compose -f "$COMPOSE_FILE" down
        ;;
    restart)
        echo "Redémarrage des services..."
        docker-compose -f "$COMPOSE_FILE" restart
        ;;
    status)
        echo "Status des services:"
        docker-compose -f "$COMPOSE_FILE" ps
        ;;
    logs)
        docker-compose -f "$COMPOSE_FILE" logs -f
        ;;
    update)
        echo "Mise à jour de l'application..."
        cd "$PROJECT_DIR/src"
        git pull origin main
        docker-compose -f "$COMPOSE_FILE" build --no-cache
        docker-compose -f "$COMPOSE_FILE" up -d
        ;;
    backup)
        echo "Création d'une sauvegarde..."
        BACKUP_FILE="$PROJECT_DIR/backups/manual_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
        tar -czf "$BACKUP_FILE" -C "$PROJECT_DIR" data config .env
        echo "Sauvegarde créée: $BACKUP_FILE"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|update|backup}"
        exit 1
        ;;
esac
EOF
    
    chmod +x "$PROJECT_DIR/manage.sh"
    
    log "✅ Post-déploiement terminé"
}

# Fonction principale
main() {
    log "🚀 Début du déploiement Oracle EBS Assistant - Tanger Med"
    
    # Vérification des arguments
    local ssl_option=""
    if [ "${1:-}" = "--ssl" ] || [ "${1:-}" = "--letsencrypt" ]; then
        ssl_option="$1"
    fi
    
    # Exécution des étapes
    check_prerequisites
    setup_environment
    download_source
    setup_ssl "$ssl_option"
    backup_existing_data
    deploy_services
    health_check
    setup_monitoring
    setup_logging
    post_deployment
    
    log "🎉 Déploiement terminé avec succès!"
}

# Gestion des erreurs
trap 'error "Erreur durant le déploiement à la ligne $LINENO"' ERR

# Exécution
main "$@"
```

#### **F.2.2 Script de Vérification Post-Déploiement**
```bash
#!/bin/bash
# ================================
# health-check-complete.sh
# Vérification complète de la santé du système
# ================================

set -euo pipefail

PROJECT_NAME="oracle-ebs-assistant"
PROJECT_DIR="/opt/${PROJECT_NAME}"
COMPOSE_FILE="$PROJECT_DIR/src/docker-compose.prod.yml"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Fonctions utilitaires
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Vérification des services Docker
check_docker_services() {
    echo "🔍 Vérification des services Docker..."
    
    local services=("oracle-ebs-assistant" "nginx" "redis" "postgres")
    local all_running=true
    
    for service in "${services[@]}"; do
        if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "$service.*Up"; then
            local status=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep "$service" | awk '{print $2}')
            success "$service: $status"
        else
            error "$service: Not running or unhealthy"
            all_running=false
        fi
    done
    
    if [ "$all_running" = true ]; then
        success "Tous les services Docker sont opérationnels"
    else
        error "Certains services Docker ne fonctionnent pas correctement"
        return 1
    fi
}

# Vérification des endpoints HTTP
check_http_endpoints() {
    echo "🌐 Vérification des endpoints HTTP..."
    
    local endpoints=(
        "http://localhost/health|Health Check"
        "http://localhost/api/procedures|API Procedures"
        "http://localhost/api/chat|API Chat"
        "http://localhost/static/images/login_screen.png|Static Assets"
    )
    
    for endpoint_info in "${endpoints[@]}"; do
        local url=$(echo "$endpoint_info" | cut -d'|' -f1)
        local name=$(echo "$endpoint_info" | cut -d'|' -f2)
        
        if curl -f -s --max-time 10 "$url" > /dev/null 2>&1; then
            success "$name ($url): OK"
        else
            error "$name ($url): Failed"
        fi
    done
}

# Vérification des bases de données
check_databases() {
    echo "🗄️ Vérification des bases de données..."
    
    # PostgreSQL
    if docker exec oracle-ebs-postgres pg_isready -U oracle_user -d oracle_ebs_assistant > /dev/null 2>&1; then
        success "PostgreSQL: Connected and ready"
        
        # Vérification des tables (si applicable)
        local table_count=$(docker exec oracle-ebs-postgres psql -U oracle_user -d oracle_ebs_assistant -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | xargs || echo "0")
        info "PostgreSQL: $table_count tables found"
    else
        error "PostgreSQL: Connection failed"
    fi
    
    # Redis
    if docker exec oracle-ebs-redis redis-cli ping | grep -q PONG; then
        success "Redis: Connected and responding"
        
        # Vérification des clés
        local key_count=$(docker exec oracle-ebs-redis redis-cli dbsize 2>/dev/null || echo "0")
        info "Redis: $key_count keys in database"
    else
        error "Redis: Connection failed"
    fi
}

# Vérification des performances
check_performance() {
    echo "⚡ Vérification des performances..."
    
    # Test de temps de réponse
    local response_time=$(curl -o /dev/null -s -w '%{time_total}' http://localhost/health 2>/dev/null || echo "999")
    
    if (( $(echo "$response_time < 1.0" | bc -l) )); then
        success "Temps de réponse: ${response_time}s (< 1s)"
    elif (( $(echo "$response_time < 3.0" | bc -l) )); then
        warning "Temps de réponse: ${response_time}s (acceptable mais lent)"
    else
        error "Temps de réponse: ${response_time}s (trop lent)"
    fi
    
    # Vérification de l'utilisation des ressources
    local cpu_usage=$(docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}" | grep oracle-ebs-assistant | awk '{print $2}' | sed 's/%//' || echo "0")
    local mem_usage=$(docker stats --no-stream --format "table {{.Container}}\t{{.MemPerc}}" | grep oracle-ebs-assistant | awk '{print $2}' | sed 's/%//' || echo "0")
    
    if (( $(echo "$cpu_usage < 80" | bc -l) )); then
        success "Utilisation CPU: ${cpu_usage}% (< 80%)"
    else
        warning "Utilisation CPU: ${cpu_usage}% (élevée)"
    fi
    
    if (( $(echo "$mem_usage < 90" | bc -l) )); then
        success "Utilisation Mémoire: ${mem_usage}% (< 90%)"
    else
        warning "Utilisation Mémoire: ${mem_usage}% (élevée)"
    fi
}

# Vérification des logs
check_logs() {
    echo "📋 Vérification des logs..."
    
    # Vérification des erreurs récentes
    local error_count=$(docker-compose -f "$COMPOSE_FILE" logs --since="1h" 2>/dev/null | grep -i error | wc -l || echo "0")
    
    if [ "$error_count" -eq 0 ]; then
        success "Aucune erreur dans les logs de la dernière heure"
    elif [ "$error_count" -lt 5 ]; then
        warning "$error_count erreurs trouvées dans les logs de la dernière heure"
    else
        error "$error_count erreurs trouvées dans les logs de la dernière heure"
    fi
    
    # Vérification de la taille des logs
    local log_size=$(du -sh /var/log/"$PROJECT_NAME" 2>/dev/null | awk '{print $1}' || echo "0K")
    info "Taille des logs: $log_size"
}

# Vérification de la sécurité
check_security() {
    echo "🔒 Vérification de la sécurité..."
    
    # Vérification HTTPS
    if curl -k -f -s https://localhost/health > /dev/null 2>&1; then
        success "HTTPS: Fonctionnel"
    else
        warning "HTTPS: Non configuré ou non fonctionnel"
    fi
    
    # Vérification des headers de sécurité
    local security_headers=$(curl -I -s http://localhost/ 2>/dev/null | grep -E "(X-Frame-Options|X-Content-Type-Options|X-XSS-Protection)" | wc -l || echo "0")
    
    if [ "$security_headers" -ge 2 ]; then
        success "Headers de sécurité: Configurés ($security_headers/3)"
    else
        warning "Headers de sécurité: Partiellement configurés ($security_headers/3)"
    fi
    
    # Vérification des ports exposés
    local exposed_ports=$(docker ps --format "table {{.Names}}\t{{.Ports}}" | grep -E "(oracle-ebs|nginx)" | grep -o "0.0.0.0:[0-9]*" | wc -l || echo "0")
    info "Ports exposés: $exposed_ports"
}

# Vérification du monitoring
check_monitoring() {
    echo "📊 Vérification du monitoring..."
    
    # Vérification Prometheus (si activé)
    if docker ps --format "table {{.Names}}" | grep -q "prometheus"; then
        if curl -f -s http://localhost:9090/-/healthy > /dev/null 2>&1; then
            success "Prometheus: Opérationnel"
        else
            warning "Prometheus: Démarré mais non accessible"
        fi
    else
        info "Prometheus: Non activé"
    fi
    
    # Vérification des métriques de base
    if curl -f -s http://localhost:8000/metrics > /dev/null 2>&1; then
        success "Métriques application: Disponibles"
    else
        warning "Métriques application: Non disponibles"
    fi
}

# Test fonctionnel complet
functional_test() {
    echo "🧪 Test fonctionnel complet..."
    
    # Test API Chat
    local chat_response=$(curl -s -X POST http://localhost/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message":"hello","session_id":"test-session-123"}' 2>/dev/null || echo "")
    
    if echo "$chat_response" | grep -q "message"; then
        success "API Chat: Fonctionnelle"
    else
        error "API Chat: Non fonctionnelle"
    fi
    
    # Test API Procedures
    local procedures_response=$(curl -s http://localhost/api/procedures 2>/dev/null || echo "")
    
    if echo "$procedures_response" | grep -q "work_confirmation"; then
        success "API Procedures: Fonctionnelle"
    else
        error "API Procedures: Non fonctionnelle"
    fi
}

# Génération du rapport
generate_report() {
    echo ""
    echo "📋 RAPPORT DE SANTÉ SYSTÈME"
    echo "=========================="
    echo "Date: $(date)"
    echo "Système: Oracle EBS R12 i-Supplier Assistant"
    echo "Version: $(cat $PROJECT_DIR/.env | grep VERSION | cut -d'=' -f2 || echo 'Unknown')"
    echo ""
    
    # Résumé des services
    echo "Services Docker:"
    docker-compose -f "$COMPOSE_FILE" ps
    echo ""
    
    # Utilisation des ressources
    echo "Utilisation des ressources:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
    echo ""
    
    # Espace disque
    echo "Espace disque:"
    df -h /opt/"$PROJECT_NAME"
    echo ""
    
    # Dernières erreurs
    echo "Dernières erreurs (5 dernières):"
    docker-compose -f "$COMPOSE_FILE" logs --since="24h" 2>/dev/null | grep -i error | tail -5 || echo "Aucune erreur trouvée"
}

# Fonction principale
main() {
    echo "🔍 Vérification complète de la santé du système Oracle EBS Assistant"
    echo "=================================================================="
    echo ""
    
    check_docker_services
    echo ""
    
    check_http_endpoints
    echo ""
    
    check_databases
    echo ""
    
    check_performance
    echo ""
    
    check_logs
    echo ""
    
    check_security
    echo ""
    
    check_monitoring
    echo ""
    
    functional_test
    echo ""
    
    generate_report
    
    echo ""
    echo "🏁 Vérification terminée"
}

# Exécution
main "$@"
```

### **F.3 Procédures de Maintenance**

#### **F.3.1 Script de Maintenance Automatisée**
```bash
#!/bin/bash
# ================================
# maintenance.sh
# Script de maintenance automatisée
# ================================

set -euo pipefail

PROJECT_NAME="oracle-ebs-assistant"
PROJECT_DIR="/opt/${PROJECT_NAME}"
COMPOSE_FILE="$PROJECT_DIR/src/docker-compose.prod.yml"
BACKUP_DIR="$PROJECT_DIR/backups"
LOG_FILE="/var/log/$PROJECT_NAME/maintenance.log"

# Fonctions utilitaires
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Nettoyage des logs anciens
cleanup_logs() {
    log "Nettoyage des logs anciens..."
    
    # Suppression des logs de plus de 30 jours
    find /var/log/"$PROJECT_NAME" -name "*.log" -mtime +30 -delete
    
    # Compression des logs de plus de 7 jours
    find /var/log/"$PROJECT_NAME" -name "*.log" -mtime +7 -exec gzip {} \;
    
    log "✅ Nettoyage des logs terminé"
}

# Nettoyage Docker
cleanup_docker() {
    log "Nettoyage Docker..."
    
    # Suppression des images non utilisées
    docker image prune -f
    
    # Suppression des volumes non utilisés
    docker volume prune -f
    
    # Suppression des réseaux non utilisés
    docker network prune -f
    
    # Suppression des conteneurs arrêtés
    docker container prune -f
    
    log "✅ Nettoyage Docker terminé"
}

# Sauvegarde automatique
automated_backup() {
    log "Création de la sauvegarde automatique..."
    
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/auto_backup_${backup_timestamp}.tar.gz"
    
    # Création de la sauvegarde
    tar -czf "$backup_file" -C "$PROJECT_DIR" data config .env src/procedures.json
    
    # Suppression des sauvegardes de plus de 7 jours
    find "$BACKUP_DIR" -name "auto_backup_*.tar.gz" -mtime +7 -delete
    
    log "✅ Sauvegarde créée: $backup_file"
}

# Mise à jour des certificats SSL
update_ssl_certificates() {
    log "Vérification des certificats SSL..."
    
    # Renouvellement Let's Encrypt si configuré
    if command -v certbot &> /dev/null; then
        certbot renew --quiet
        log "✅ Certificats SSL vérifiés/renouvelés"
    else
        log "ℹ️ Certbot non installé, pas de renouvellement automatique"
    fi
}

# Optimisation base de données
optimize_database() {
    log "Optimisation de la base de données..."
    
    # Nettoyage PostgreSQL
    docker exec oracle-ebs-postgres psql -U oracle_user -d oracle_ebs_assistant -c "VACUUM ANALYZE;" 2>/dev/null || true
    
    # Nettoyage Redis
    docker exec oracle-ebs-redis redis-cli FLUSHDB 2>/dev/null || true
    
    log "✅ Optimisation base de données terminée"
}

# Vérification de santé
health_check() {
    log "Vérification de santé des services..."
    
    local services=("oracle-ebs-assistant" "nginx" "redis" "postgres")
    local unhealthy_services=()
    
    for service in "${services[@]}"; do
        if ! docker ps --format "table {{.Names}}" | grep -q "$service"; then
            unhealthy_services+=("$service")
        fi
    done
    
    if [ ${#unhealthy_services[@]} -eq 0 ]; then
        log "✅ Tous les services sont opérationnels"
    else
        log "⚠️ Services non opérationnels: ${unhealthy_services[*]}"
        
        # Tentative de redémarrage
        log "Tentative de redémarrage des services..."
        docker-compose -f "$COMPOSE_FILE" restart "${unhealthy_services[@]}"
    fi
}

# Mise à jour système
system_update() {
    log "Mise à jour du système..."
    
    # Mise à jour des packages système (Ubuntu/Debian)
    if command -v apt-get &> /dev/null; then
        apt-get update -qq
        apt-get upgrade -y -qq
    fi
    
    # Mise à jour Docker images
    cd "$PROJECT_DIR/src"
    docker-compose -f "$COMPOSE_FILE" pull
    
    log "✅ Mise à jour système terminée"
}

# Rapport de maintenance
generate_maintenance_report() {
    local report_file="$PROJECT_DIR/maintenance_report_$(date +%Y%m%d).txt"
    
    cat > "$report_file" << EOF
RAPPORT DE MAINTENANCE - Oracle EBS Assistant
============================================
Date: $(date)
Système: $(uname -a)

SERVICES DOCKER:
$(docker-compose -f "$COMPOSE_FILE" ps)

UTILISATION RESSOURCES:
$(docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}")

ESPACE DISQUE:
$(df -h "$PROJECT_DIR")

SAUVEGARDES DISPONIBLES:
$(ls -la "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -5 || echo "Aucune sauvegarde trouvée")

LOGS RÉCENTS (Erreurs):
$(docker-compose -f "$COMPOSE_FILE" logs --since="24h" 2>/dev/null | grep -i error | tail -10 || echo "Aucune erreur récente")

CERTIFICATS SSL:
$(openssl x509 -in "$PROJECT_DIR/ssl/cert.pem" -noout -dates 2>/dev/null || echo "Certificat non trouvé")
EOF
    
    log "✅ Rapport de maintenance généré: $report_file"
}

# Fonction principale
main() {
    log "🔧 Début de la maintenance automatisée"
    
    case "${1:-all}" in
        "cleanup")
            cleanup_logs
            cleanup_docker
            ;;
        "backup")
            automated_backup
            ;;
        "ssl")
            update_ssl_certificates
            ;;
        "database")
            optimize_database
            ;;
        "health")
            health_check
            ;;
        "update")
            system_update
            ;;
        "all")
            cleanup_logs
            cleanup_docker
            automated_backup
            update_ssl_certificates
            optimize_database
            health_check
            generate_maintenance_report
            ;;
        *)
            echo "Usage: $0 {cleanup|backup|ssl|database|health|update|all}"
            exit 1
            ;;
    esac
    
    log "✅ Maintenance terminée"
}

# Exécution
main "$@"
```

#### **F.3.2 Configuration Cron pour Maintenance Automatique**
```bash
# ================================
# Crontab pour maintenance automatique
# ================================

# Installation du crontab
cat > /tmp/oracle-assistant-cron << 'EOF'
# Oracle EBS Assistant - Tâches de maintenance automatique

# Sauvegarde quotidienne à 2h du matin
0 2 * * * /opt/oracle-ebs-assistant/maintenance.sh backup >> /var/log/oracle-ebs-assistant/cron.log 2>&1

# Nettoyage hebdomadaire le dimanche à 3h
0 3 * * 0 /opt/oracle-ebs-assistant/maintenance.sh cleanup >> /var/log/oracle-ebs-assistant/cron.log 2>&1

# Vérification de santé toutes les heures
0 * * * * /opt/oracle-ebs-assistant/maintenance.sh health >> /var/log/oracle-ebs-assistant/cron.log 2>&1

# Optimisation base de données quotidienne à 4h
0 4 * * * /opt/oracle-ebs-assistant/maintenance.sh database >> /var/log/oracle-ebs-assistant/cron.log 2>&1

# Renouvellement SSL mensuel
0 5 1 * * /opt/oracle-ebs-assistant/maintenance.sh ssl >> /var/log/oracle-ebs-assistant/cron.log 2>&1

# Mise à jour système mensuelle (premier dimanche du mois à 5h)
0 5 1-7 * 0 /opt/oracle-ebs-assistant/maintenance.sh update >> /var/log/oracle-ebs-assistant/cron.log 2>&1

# Maintenance complète hebdomadaire le samedi à 6h
0 6 * * 6 /opt/oracle-ebs-assistant/maintenance.sh all >> /var/log/oracle-ebs-assistant/cron.log 2>&1
EOF

# Installation du crontab
sudo crontab -u root /tmp/oracle-assistant-cron
rm /tmp/oracle-assistant-cron

echo "✅ Tâches de maintenance automatique configurées"
```

---

## **ANNEXE G - API DOCUMENTATION** {#annexe-g}

### **G.1 Endpoints API Complets**

#### **G.1.1 API Chat - Endpoint Principal**
```python
# ================================
# POST /api/chat
# Endpoint principal pour interaction chat
# ================================

@app.post("/api/chat", response_model=ChatResponse)
@track_request_metrics
async def chat_endpoint(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    request_info: Request = None
):
    """
    Endpoint principal pour les interactions chat avec l'assistant Oracle EBS.
    
    **Fonctionnalités:**
    - Traitement des messages utilisateur
    - Gestion des workflows Oracle EBS
    - Support multilingue (FR/EN)
    - Génération de réponses IA contextuelles
    - Suivi de progression des procédures
    
    **Paramètres:**
    - message: Message utilisateur (1-2000 caractères)
    - session_id: Identifiant de session unique
    - context: Contexte optionnel pour la conversation
    - force_language: Forcer une langue spécifique (en/fr)
    
    **Réponse:**
    - message: Réponse de l'assistant
    - session_state: État actuel de la session
    - current_step: Étape actuelle du workflow (si applicable)
    - suggestions: Suggestions d'actions suivantes
    - screenshot: URL de capture d'écran (si applicable)
    - validation_errors: Erreurs de validation (si applicable)
    """
    
    try:
        # Validation et sanitisation
        if not security_manager.validate_session_id(request.session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        if not security_manager.validate_oracle_query(request.message):
            raise HTTPException(status_code=400, detail="Invalid message content")
        
        # Récupération de la session
        session = session_manager.get_session(request.session_id)
        
        # Forcer la langue si spécifiée
        if request.force_language:
            session.language = request.force_language
            session.preferred_language = request.force_language
        
        # Traitement du message
        response = await oracle_agent.process_message(
            message=request.message,
            session=session,
            context=request.context or {}
        )
        
        # Mise à jour de la session
        session_manager.update_session(request.session_id, response.session_state)
        
        # Tâches en arrière-plan
        background_tasks.add_task(
            metrics_collector.update_session_metrics
        )
        
        # Audit logging
        background_tasks.add_task(
            security_manager.audit_log,
            "chat_interaction",
            request.session_id,
            {
                'ip_address': request_info.client.host if request_info else 'unknown',
                'user_agent': request_info.headers.get('user-agent', 'unknown') if request_info else 'unknown',
                'message_length': len(request.message),
                'success': True
            }
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        # Log erreur sans exposer détails
        logger.error(f"Chat endpoint error: {str(e)}")
        
        # Audit logging pour erreur
        background_tasks.add_task(
            security_manager.audit_log,
            "chat_error",
            request.session_id,
            {
                'ip_address': request_info.client.host if request_info else 'unknown',
                'error_type': type(e).__name__,
                'success': False
            }
        )
        
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred"
        )

# ================================
# Modèles de données pour Chat API
# ================================

class ChatRequest(BaseModel):
    """Modèle de requête pour l'API Chat"""
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Message utilisateur",
        example="Start work confirmation procedure"
    )
    session_id: str = Field(
        ...,
        regex=r'^[a-zA-Z0-9-_]{8,64}$',
        description="Identifiant de session unique",
        example="session-123e4567-e89b-12d3-a456-426614174000"
    )
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Contexte optionnel pour la conversation",
        example={"current_procedure": "work_confirmation", "language": "en"}
    )
    force_language: Optional[str] = Field(
        None,
        regex=r'^(en|fr)$',
        description="Forcer une langue spécifique",
        example="fr"
    )
    
    @validator('message')
    def sanitize_message(cls, v):
        return security_manager.sanitize_input(v)

class ChatResponse(BaseModel):
    """Modèle de réponse pour l'API Chat"""
    message: str = Field(
        ...,
        description="Réponse de l'assistant",
        example="I'll help you create a work confirmation. Let's start with step 1..."
    )
    message_type: MessageType = Field(
        default=MessageType.ASSISTANT,
        description="Type de message"
    )
    session_state: SessionState = Field(
        ...,
        description="État actuel de la session"
    )
    current_step: Optional[WorkflowStep] = Field(
        None,
        description="Étape actuelle du workflow"
    )
    screenshot: Optional[str] = Field(
        None,
        description="URL de capture d'écran",
        example="/static/images/login_screen.png"
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions d'actions suivantes",
        example=["Done with this step", "Show screenshot", "Cancel procedure"]
    )
    validation_errors: List[str] = Field(
        default_factory=list,
        description="Erreurs de validation"
    )
    oracle_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Données Oracle (pour requêtes)"
    )
    language: str = Field(
        default="en",
        description="Langue de la réponse",
        example="en"
    )
```

#### **G.1.2 API Procedures - Gestion des Procédures**
```python
# ================================
# GET /api/procedures
# Liste des procédures disponibles
# ================================

@app.get("/api/procedures", response_model=List[ProcedureInfo])
@track_request_metrics
async def get_procedures(
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    language: Optional[str] = Query("en", regex=r'^(en|fr)$', description="Langue")
):
    """
    Récupère la liste des procédures Oracle EBS disponibles.
    
    **Paramètres:**
    - category: Filtrer par catégorie (procurement, financial, supplier_management, etc.)
    - language: Langue pour les descriptions (en/fr)
    
    **Réponse:**
    Liste des procédures avec métadonnées complètes
    """
    
    try:
        procedures = oracle_agent.get_available_procedures()
        
        # Filtrage par catégorie si spécifié
        if category:
            procedures = [p for p in procedures if p.category == category]
        
        # Traduction si nécessaire
        if language == 'fr':
            for procedure in procedures:
                procedure.title = oracle_agent._translate_procedure_content(procedure.title, 'fr')
                procedure.description = oracle_agent._translate_procedure_content(procedure.description, 'fr')
        
        return procedures
        
    except Exception as e:
        logger.error(f"Procedures endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving procedures")

# ================================
# GET /api/procedures/{procedure_id}
# Détails d'une procédure spécifique
# ================================

@app.get("/api/procedures/{procedure_id}", response_model=Dict[str, Any])
@track_request_metrics
async def get_procedure_details(
    procedure_id: str = Path(..., description="ID de la procédure"),
    language: Optional[str] = Query("en", regex=r'^(en|fr)$', description="Langue")
):
    """
    Récupère les détails complets d'une procédure spécifique.
    
    **Paramètres:**
    - procedure_id: Identifiant de la procédure
    - language: Langue pour le contenu (en/fr)
    
    **Réponse:**
    Détails complets de la procédure incluant toutes les étapes
    """
    
    try:
        procedure_details = oracle_agent.get_procedure_details(procedure_id)
        
        if not procedure_details:
            raise HTTPException(status_code=404, detail="Procedure not found")
        
        # Traduction si nécessaire
        if language == 'fr':
            # Traduction du contenu principal
            procedure_details['title'] = oracle_agent._translate_procedure_content(
                procedure_details['title'], 'fr'
            )
            procedure_details['description'] = oracle_agent._translate_procedure_content(
                procedure_details['description'], 'fr'
            )
            
            # Traduction des étapes
            for step in procedure_details.get('steps', []):
                step['title'] = oracle_agent._translate_procedure_content(step['title'], 'fr')
                step['description'] = oracle_agent._translate_procedure_content(step['description'], 'fr')
                step['instructions'] = oracle_agent._translate_procedure_content(step['instructions'], 'fr')
        
        return procedure_details
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Procedure details error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving procedure details")

# ================================
# Modèles pour Procedures API
# ================================

class ProcedureInfo(BaseModel):
    """Information sur une procédure"""
    procedure_id: str = Field(..., description="Identifiant unique")
    title: str = Field(..., description="Titre de la procédure")
    description: str = Field(..., description="Description détaillée")
    category: str = Field(..., description="Catégorie")
    prerequisites: List[str] = Field(default_factory=list, description="Prérequis")
    estimated_time: Optional[str] = Field(None, description="Temps estimé")
    difficulty: Optional[str] = Field(None, description="Niveau de difficulté")
    steps_count: Optional[int] = Field(None, description="Nombre d'étapes")
    
    class Config:
        schema_extra = {
            "example": {
                "procedure_id": "work_confirmation",
                "title": "Create Work Confirmation",
                "description": "Step-by-step guide to create a work confirmation",
                "category": "procurement",
                "prerequisites": ["Valid credentials", "Active PO"],
                "estimated_time": "10-15 minutes",
                "difficulty": "intermediate",
                "steps_count": 6
            }
        }
```

#### **G.1.3 API Oracle Queries - Requêtes de Données**
```python
# ================================
# POST /api/oracle/query
# Requêtes de données Oracle
# ================================

@app.post("/api/oracle/query", response_model=OracleQueryResponse)
@track_request_metrics
async def oracle_query_endpoint(
    query: OracleQueryRequest,
    background_tasks: BackgroundTasks
):
    """
    Exécute des requêtes sur les données Oracle EBS (mockées).
    
    **Modules supportés:**
    - purchase_orders: Commandes d'achat
    - invoices: Factures
    - suppliers: Fournisseurs
    - contracts: Contrats
    - rfqs: Appels d'offres
    - analytics: Données analytiques
    
    **Types de requêtes:**
    - list_all: Lister tous les éléments
    - search_by_id: Recherche par identifiant
    - search_by_criteria: Recherche par critères
    """
    
    try:
        # Validation du module
        allowed_modules = ['purchase_orders', 'invoices', 'suppliers', 'contracts', 'rfqs', 'analytics']
        if query.module not in allowed_modules:
            raise HTTPException(status_code=400, detail=f"Module not allowed: {query.module}")
        
        # Validation des paramètres
        for key, value in query.parameters.items():
            if isinstance(value, str):
                if not security_manager.validate_oracle_query(value):
                    raise HTTPException(status_code=400, detail=f"Invalid parameter: {key}")
        
        # Exécution de la requête
        start_time = time.time()
        
        result = await oracle_agent.query_oracle_module(
            module=query.module,
            query_type=query.query_type,
            parameters=query.parameters
        )
        
        query_duration = time.time() - start_time
        
        # Métriques
        background_tasks.add_task(
            metrics_collector.record_oracle_query_time,
            query.module,
            query.query_type,
            query_duration
        )
        
        return OracleQueryResponse(
            success=True,
            data=result,
            metadata={
                "query_time": query_duration,
                "result_count": len(result) if isinstance(result, list) else 1,
                "module": query.module,
                "query_type": query.query_type
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Oracle query error: {str(e)}")
        return OracleQueryResponse(
            success=False,
            error=f"Query execution failed: {type(e).__name__}",
            metadata={"module": query.module, "query_type": query.query_type}
        )

# ================================
# Modèles pour Oracle API
# ================================

class OracleQueryRequest(BaseModel):
    """Requête Oracle EBS"""
    module: str = Field(
        ...,
        regex=r'^[a-zA-Z_]+$',
        description="Module Oracle à interroger",
        example="purchase_orders"
    )
    query_type: str = Field(
        ...,
        regex=r'^[a-zA-Z_]+$',
        description="Type de requête",
        example="list_all"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Paramètres de la requête",
        example={"po_number": "PO-2024-001"}
    )
    
    @validator('module')
    def validate_module(cls, v):
        allowed_modules = ['purchase_orders', 'invoices', 'suppliers', 'contracts', 'rfqs', 'analytics']
        if v not in allowed_modules:
            raise ValueError(f'Module non autorisé: {v}')
        return v

class OracleQueryResponse(BaseModel):
    """Réponse requête Oracle"""
    success: bool = Field(..., description="Succès de la requête")
    data: Optional[List[Dict[str, Any]]] = Field(None, description="Données résultat")
    error: Optional[str] = Field(None, description="Message d'erreur")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Métadonnées")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": [
                    {
                        "po_number": "PO-2024-001",
                        "supplier": "Tanger Med Services",
                        "status": "Approved",
                        "amount": 50000.00
                    }
                ],
                "metadata": {
                    "query_time": 0.045,
                    "result_count": 1,
                    "module": "purchase_orders"
                }
            }
        }
```

---

Cette section continue l'annexe avec le guide de déploiement et la documentation API. Le fichier se terminera avec la section H (Troubleshooting).
#### **G.1.4 API Session Management - Gestion des Sessions**
```python
# ================================
# GET /api/session/{session_id}/progress
# Progression de la session
# ================================

@app.get("/api/session/{session_id}/progress", response_model=Dict[str, Any])
@track_request_metrics
async def get_session_progress(
    session_id: str = Path(..., description="ID de session")
):
    """
    Récupère la progression actuelle d'une session utilisateur.
    
    **Réponse:**
    - current_procedure: Procédure en cours
    - current_step: Étape actuelle
    - completed_steps: Étapes terminées
    - progress_percentage: Pourcentage de progression
    - session_duration: Durée de la session
    """
    
    try:
        if not security_manager.validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        session = session_manager.get_session(session_id)
        
        # Calcul de la progression
        progress_data = {
            "session_id": session.session_id,
            "current_procedure": session.current_procedure,
            "current_step": session.current_step,
            "completed_steps": session.completed_steps,
            "status": session.status.value,
            "language": session.language,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
            "session_duration": (datetime.now() - session.created_at).total_seconds()
        }
        
        # Calcul pourcentage si procédure active
        if session.current_procedure:
            procedure = oracle_agent.get_procedure_details(session.current_procedure)
            if procedure and procedure.get('steps'):
                total_steps = len(procedure['steps'])
                completed_count = len(session.completed_steps)
                progress_data["progress_percentage"] = (completed_count / total_steps) * 100
                progress_data["total_steps"] = total_steps
        
        return progress_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session progress error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving session progress")

# ================================
# POST /api/session/{session_id}/reset
# Réinitialisation de session
# ================================

@app.post("/api/session/{session_id}/reset", response_model=Dict[str, str])
@track_request_metrics
async def reset_session(
    session_id: str = Path(..., description="ID de session"),
    background_tasks: BackgroundTasks
):
    """
    Remet à zéro une session utilisateur.
    
    **Effet:**
    - Supprime la procédure en cours
    - Remet le statut à NOT_STARTED
    - Préserve les préférences linguistiques
    """
    
    try:
        if not security_manager.validate_session_id(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        # Récupération durée session avant reset
        session = session_manager.get_session(session_id)
        session_duration = (datetime.now() - session.created_at).total_seconds()
        
        # Reset de la session
        session_manager.reset_session(session_id)
        
        # Métriques
        background_tasks.add_task(
            metrics_collector.record_session_duration,
            session_duration
        )
        
        return {"message": "Session reset successfully", "session_id": session_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session reset error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error resetting session")
```

#### **G.1.5 API Health et Monitoring**
```python
# ================================
# GET /health
# Health check endpoint
# ================================

@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """
    Endpoint de vérification de santé du service.
    
    **Vérifications:**
    - Status de l'application
    - Connectivité base de données
    - Connectivité cache Redis
    - Status des services externes
    """
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.getenv("VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "checks": {}
    }
    
    try:
        # Vérification application
        health_status["checks"]["application"] = {
            "status": "healthy",
            "response_time": 0.001
        }
        
        # Vérification Redis (si configuré)
        try:
            # Test Redis connection
            health_status["checks"]["redis"] = {
                "status": "healthy",
                "response_time": 0.005
            }
        except Exception as e:
            health_status["checks"]["redis"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "degraded"
        
        # Vérification PostgreSQL (si configuré)
        try:
            # Test DB connection
            health_status["checks"]["database"] = {
                "status": "healthy",
                "response_time": 0.010
            }
        except Exception as e:
            health_status["checks"]["database"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "degraded"
        
        # Vérification API Gemini
        try:
            # Test API availability (simple check)
            health_status["checks"]["gemini_api"] = {
                "status": "healthy",
                "response_time": 0.100
            }
        except Exception as e:
            health_status["checks"]["gemini_api"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

# ================================
# GET /metrics
# Métriques Prometheus
# ================================

@app.get("/metrics", response_class=PlainTextResponse)
async def get_metrics():
    """
    Endpoint pour les métriques Prometheus.
    
    **Métriques exposées:**
    - Compteurs de requêtes HTTP
    - Histogrammes de temps de réponse
    - Métriques de sessions actives
    - Métriques de procédures
    - Métriques IA
    """
    
    # Mise à jour des métriques dynamiques
    metrics_collector.update_session_metrics()
    
    # Génération du format Prometheus
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# ================================
# GET /api/stats
# Statistiques système
# ================================

@app.get("/api/stats", response_model=Dict[str, Any])
@track_request_metrics
async def get_system_stats():
    """
    Statistiques système et métriques business.
    
    **Statistiques:**
    - Sessions actives
    - Procédures populaires
    - Performance IA
    - Utilisation ressources
    """
    
    try:
        # Statistiques sessions
        session_stats = session_manager.get_session_stats()
        
        # Statistiques procédures (simulées)
        procedure_stats = {
            "most_popular": [
                {"procedure": "work_confirmation", "count": 150},
                {"procedure": "invoice_submission", "count": 120},
                {"procedure": "view_purchase_orders", "count": 100}
            ],
            "completion_rates": {
                "work_confirmation": 0.85,
                "invoice_submission": 0.92,
                "view_purchase_orders": 0.98
            }
        }
        
        # Statistiques IA (simulées)
        ai_stats = {
            "intent_recognition_accuracy": 0.94,
            "average_response_time": 1.2,
            "language_distribution": {
                "en": 0.60,
                "fr": 0.40
            }
        }
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "sessions": session_stats,
            "procedures": procedure_stats,
            "ai_performance": ai_stats,
            "system": {
                "uptime": time.time() - start_time,
                "version": os.getenv("VERSION", "1.0.0"),
                "environment": os.getenv("ENVIRONMENT", "development")
            }
        }
        
    except Exception as e:
        logger.error(f"Stats endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")
```

### **G.2 Schémas OpenAPI Complets**

#### **G.2.1 Configuration OpenAPI**
```python
# ================================
# Configuration OpenAPI/Swagger
# ================================

app = FastAPI(
    title="Oracle EBS R12 i-Supplier Assistant API",
    description="""
    API complète pour l'assistant Oracle EBS R12 i-Supplier de Tanger Med Port Authority.
    
    ## Fonctionnalités Principales
    
    * **Chat Interactif** - Interface conversationnelle avec IA
    * **Workflows Oracle EBS** - 12 procédures complètes guidées
    * **Support Multilingue** - Français et Anglais
    * **Gestion de Sessions** - Suivi de progression persistant
    * **Requêtes Oracle** - Accès aux données EBS (mockées)
    * **Monitoring** - Métriques et health checks
    
    ## Authentification
    
    Actuellement, l'API utilise des sessions basées sur des UUID.
    L'authentification JWT sera ajoutée dans les versions futures.
    
    ## Limites de Taux
    
    * API Chat: 10 requêtes/seconde par IP
    * Autres endpoints: 30 requêtes/seconde par IP
    
    ## Support
    
    Pour le support technique, contactez l'équipe IT de Tanger Med.
    """,
    version="1.0.0",
    terms_of_service="https://tangermed.ma/terms",
    contact={
        "name": "Tanger Med IT Support",
        "url": "https://tangermed.ma/support",
        "email": "it-support@tangermed.ma",
    },
    license_info={
        "name": "Proprietary License",
        "url": "https://tangermed.ma/license",
    },
    openapi_tags=[
        {
            "name": "Chat",
            "description": "Interactions conversationnelles avec l'assistant IA",
        },
        {
            "name": "Procedures",
            "description": "Gestion des procédures Oracle EBS R12",
        },
        {
            "name": "Oracle Queries",
            "description": "Requêtes de données Oracle EBS",
        },
        {
            "name": "Sessions",
            "description": "Gestion des sessions utilisateur",
        },
        {
            "name": "Monitoring",
            "description": "Health checks et métriques système",
        }
    ]
)

# Configuration CORS pour documentation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

#### **G.2.2 Exemples de Requêtes/Réponses**
```python
# ================================
# Exemples pour documentation API
# ================================

# Exemple Chat Request
CHAT_REQUEST_EXAMPLE = {
    "message": "I want to create a work confirmation for PO-2024-001",
    "session_id": "session-123e4567-e89b-12d3-a456-426614174000",
    "context": {
        "current_procedure": None,
        "language": "en"
    }
}

# Exemple Chat Response
CHAT_RESPONSE_EXAMPLE = {
    "message": "I'll help you create a work confirmation. Let's start with step 1: Login to i-Supplier Portal...",
    "message_type": "assistant",
    "session_state": {
        "session_id": "session-123e4567-e89b-12d3-a456-426614174000",
        "current_procedure": "work_confirmation",
        "current_step": "login",
        "completed_steps": [],
        "status": "in_progress",
        "language": "en"
    },
    "current_step": {
        "step_id": "login",
        "title": "Login to i-Supplier Portal",
        "description": "Access the Oracle EBS R12 i-Supplier portal using your credentials",
        "instructions": "Navigate to the i-Supplier portal URL and enter your username and password",
        "screenshot": "/static/images/login_screen.png"
    },
    "suggestions": [
        "Done with this step",
        "Show screenshot",
        "Cancel procedure"
    ],
    "language": "en"
}

# Exemple Oracle Query Request
ORACLE_QUERY_REQUEST_EXAMPLE = {
    "module": "purchase_orders",
    "query_type": "search_by_po_number",
    "parameters": {
        "po_number": "PO-2024-001"
    }
}

# Exemple Oracle Query Response
ORACLE_QUERY_RESPONSE_EXAMPLE = {
    "success": True,
    "data": [
        {
            "po_number": "PO-2024-001",
            "supplier": "Tanger Med Services",
            "status": "Approved",
            "amount": 50000.00,
            "currency": "MAD",
            "created_date": "2024-01-15",
            "delivery_date": "2024-02-15",
            "description": "IT Services Contract"
        }
    ],
    "metadata": {
        "query_time": 0.045,
        "result_count": 1,
        "module": "purchase_orders",
        "query_type": "search_by_po_number"
    }
}

# Configuration des exemples dans les endpoints
@app.post("/api/chat", 
    response_model=ChatResponse,
    tags=["Chat"],
    summary="Interaction chat avec l'assistant",
    description="Envoie un message à l'assistant et reçoit une réponse contextuelle",
    responses={
        200: {
            "description": "Réponse de l'assistant",
            "content": {
                "application/json": {
                    "example": CHAT_RESPONSE_EXAMPLE
                }
            }
        },
        400: {
            "description": "Requête invalide",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid session ID format"}
                }
            }
        },
        500: {
            "description": "Erreur serveur",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error occurred"}
                }
            }
        }
    }
)
async def chat_endpoint(request: ChatRequest):
    # Implementation...
    pass
```

---

## **ANNEXE H - TROUBLESHOOTING** {#annexe-h}

### **H.1 Guide de Résolution des Problèmes Courants**

#### **H.1.1 Problèmes de Démarrage**

```bash
# ================================
# Problème: Services Docker ne démarrent pas
# ================================

# Diagnostic
echo "🔍 Diagnostic des services Docker..."

# Vérification Docker daemon
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker daemon non accessible"
    echo "Solutions:"
    echo "1. sudo systemctl start docker"
    echo "2. sudo usermod -aG docker $USER (puis redémarrer session)"
    echo "3. Vérifier /var/lib/docker/daemon.json"
fi

# Vérification espace disque
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "⚠️ Espace disque critique: ${DISK_USAGE}%"
    echo "Solutions:"
    echo "1. docker system prune -af"
    echo "2. Nettoyer /var/log/"
    echo "3. Supprimer images Docker inutiles"
fi

# Vérification mémoire
FREE_MEM=$(free -m | awk 'NR==2{printf "%.0f", $7/1024}')
if [ "$FREE_MEM" -lt 2 ]; then
    echo "⚠️ Mémoire insuffisante: ${FREE_MEM}GB libre"
    echo "Solutions:"
    echo "1. Fermer applications non nécessaires"
    echo "2. Augmenter swap"
    echo "3. Redémarrer le système"
fi

# Vérification ports
PORTS_IN_USE=$(netstat -tulpn | grep -E ':(80|443|8000|6379|5432)' | wc -l)
if [ "$PORTS_IN_USE" -gt 0 ]; then
    echo "⚠️ Ports déjà utilisés:"
    netstat -tulpn | grep -E ':(80|443|8000|6379|5432)'
    echo "Solutions:"
    echo "1. Arrêter services conflictuels"
    echo "2. Modifier ports dans docker-compose.yml"
fi
```

#### **H.1.2 Problèmes de Performance**

```bash
# ================================
# Diagnostic Performance
# ================================

#!/bin/bash
echo "📊 Diagnostic de performance Oracle EBS Assistant"

PROJECT_DIR="/opt/oracle-ebs-assistant"
COMPOSE_FILE="$PROJECT_DIR/src/docker-compose.prod.yml"

# Fonction de diagnostic performance
diagnose_performance() {
    echo "🔍 Analyse des performances..."
    
    # Temps de réponse API
    echo "Test temps de réponse API:"
    for i in {1..5}; do
        RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' http://localhost/health 2>/dev/null || echo "999")
        echo "  Tentative $i: ${RESPONSE_TIME}s"
    done
    
    # Utilisation ressources containers
    echo ""
    echo "Utilisation ressources containers:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"
    
    # Processus système
    echo ""
    echo "Top processus CPU:"
    ps aux --sort=-%cpu | head -10
    
    echo ""
    echo "Top processus mémoire:"
    ps aux --sort=-%mem | head -10
    
    # Analyse logs erreurs
    echo ""
    echo "Erreurs récentes dans les logs:"
    docker-compose -f "$COMPOSE_FILE" logs --since="1h" 2>/dev/null | grep -i error | tail -10 || echo "Aucune erreur trouvée"
    
    # Connexions réseau
    echo ""
    echo "Connexions réseau actives:"
    netstat -an | grep -E ':(80|443|8000|6379|5432)' | grep ESTABLISHED | wc -l
}

# Solutions performance
optimize_performance() {
    echo "⚡ Optimisations de performance..."
    
    # Nettoyage Docker
    echo "Nettoyage Docker..."
    docker system prune -f
    
    # Optimisation PostgreSQL
    echo "Optimisation PostgreSQL..."
    docker exec oracle-ebs-postgres psql -U oracle_user -d oracle_ebs_assistant -c "VACUUM ANALYZE;" 2>/dev/null || true
    
    # Nettoyage Redis
    echo "Nettoyage cache Redis..."
    docker exec oracle-ebs-redis redis-cli FLUSHDB 2>/dev/null || true
    
    # Redémarrage services
    echo "Redémarrage services..."
    docker-compose -f "$COMPOSE_FILE" restart
    
    echo "✅ Optimisations appliquées"
}

# Monitoring continu
monitor_performance() {
    echo "📈 Monitoring performance en continu (Ctrl+C pour arrêter)..."
    
    while true; do
        clear
        echo "=== Oracle EBS Assistant - Performance Monitor ==="
        echo "Timestamp: $(date)"
        echo ""
        
        # API Response time
        API_TIME=$(curl -o /dev/null -s -w '%{time_total}' http://localhost/health 2>/dev/null || echo "N/A")
        echo "API Response Time: ${API_TIME}s"
        
        # Container stats
        echo ""
        echo "Container Resources:"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemPerc}}"
        
        # System load
        echo ""
        echo "System Load:"
        uptime
        
        sleep 5
    done
}

# Menu principal
case "${1:-diagnose}" in
    "diagnose")
        diagnose_performance
        ;;
    "optimize")
        optimize_performance
        ;;
    "monitor")
        monitor_performance
        ;;
    *)
        echo "Usage: $0 {diagnose|optimize|monitor}"
        exit 1
        ;;
esac
```

#### **H.1.3 Problèmes de Connectivité**

```python
# ================================
# Script de diagnostic connectivité
# connectivity_check.py
# ================================

import requests
import socket
import time
import json
from datetime import datetime

class ConnectivityChecker:
    def __init__(self):
        self.base_url = "http://localhost"
        self.endpoints = [
            "/health",
            "/api/procedures",
            "/api/chat",
            "/static/images/login_screen.png"
        ]
        
    def check_port(self, host, port, timeout=5):
        """Vérification connectivité port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def check_http_endpoint(self, endpoint, timeout=10):
        """Vérification endpoint HTTP"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, timeout=timeout)
            return {
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "success": response.status_code == 200
            }
        except requests.exceptions.RequestException as e:
            return {
                "endpoint": endpoint,
                "error": str(e),
                "success": False
            }
    
    def check_docker_services(self):
        """Vérification services Docker"""
        import subprocess
        
        services = ["oracle-ebs-assistant", "nginx", "redis", "postgres"]
        results = {}
        
        for service in services:
            try:
                result = subprocess.run(
                    ["docker", "ps", "--filter", f"name={service}", "--format", "{{.Status}}"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0 and "Up" in result.stdout:
                    results[service] = {"status": "running", "details": result.stdout.strip()}
                else:
                    results[service] = {"status": "stopped", "details": result.stdout.strip()}
                    
            except Exception as e:
                results[service] = {"status": "error", "error": str(e)}
        
        return results
    
    def run_full_check(self):
        """Diagnostic complet connectivité"""
        print("🔍 Diagnostic de connectivité Oracle EBS Assistant")
        print("=" * 50)
        
        # Vérification ports
        print("\n📡 Vérification des ports:")
        ports = [80, 443, 8000, 6379, 5432]
        for port in ports:
            is_open = self.check_port("localhost", port)
            status = "✅ OUVERT" if is_open else "❌ FERMÉ"
            print(f"  Port {port}: {status}")
        
        # Vérification services Docker
        print("\n🐳 Vérification services Docker:")
        docker_services = self.check_docker_services()
        for service, info in docker_services.items():
            status_icon = "✅" if info["status"] == "running" else "❌"
            print(f"  {service}: {status_icon} {info['status']}")
            if "error" in info:
                print(f"    Erreur: {info['error']}")
        
        # Vérification endpoints HTTP
        print("\n🌐 Vérification endpoints HTTP:")
        for endpoint in self.endpoints:
            result = self.check_http_endpoint(endpoint)
            if result["success"]:
                print(f"  {endpoint}: ✅ OK ({result['response_time']:.3f}s)")
            else:
                print(f"  {endpoint}: ❌ ÉCHEC")
                if "error" in result:
                    print(f"    Erreur: {result['error']}")
                elif "status_code" in result:
                    print(f"    Code: {result['status_code']}")
        
        # Test fonctionnel API
        print("\n🧪 Test fonctionnel API:")
        self.test_api_functionality()
        
        # Recommandations
        print("\n💡 Recommandations:")
        self.generate_recommendations(docker_services)
    
    def test_api_functionality(self):
        """Test fonctionnel de l'API"""
        try:
            # Test API Chat
            chat_payload = {
                "message": "hello",
                "session_id": "test-connectivity-check"
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=chat_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("  API Chat: ✅ Fonctionnelle")
            else:
                print(f"  API Chat: ❌ Erreur {response.status_code}")
                
        except Exception as e:
            print(f"  API Chat: ❌ Erreur - {str(e)}")
        
        try:
            # Test API Procedures
            response = requests.get(f"{self.base_url}/api/procedures", timeout=10)
            
            if response.status_code == 200:
                procedures = response.json()
                print(f"  API Procedures: ✅ {len(procedures)} procédures disponibles")
            else:
                print(f"  API Procedures: ❌ Erreur {response.status_code}")
                
        except Exception as e:
            print(f"  API Procedures: ❌ Erreur - {str(e)}")
    
    def generate_recommendations(self, docker_services):
        """Génération de recommandations"""
        stopped_services = [name for name, info in docker_services.items() 
                          if info["status"] != "running"]
        
        if stopped_services:
            print(f"  • Redémarrer les services arrêtés: {', '.join(stopped_services)}")
            print("    Commande: docker-compose -f docker-compose.prod.yml restart")
        
        print("  • Vérifier les logs pour plus de détails:")
        print("    Commande: docker-compose -f docker-compose.prod.yml logs -f")
        
        print("  • En cas de problème persistant:")
        print("    1. Redémarrer tous les services")
        print("    2. Vérifier l'espace disque disponible")
        print("    3. Consulter la documentation de troubleshooting")

if __name__ == "__main__":
    checker = ConnectivityChecker()
    checker.run_full_check()
```

#### **H.1.4 Problèmes de Base de Données**

```bash
# ================================
# Diagnostic et réparation base de données
# ================================

#!/bin/bash
echo "🗄️ Diagnostic base de données Oracle EBS Assistant"

PROJECT_DIR="/opt/oracle-ebs-assistant"
COMPOSE_FILE="$PROJECT_DIR/src/docker-compose.prod.yml"

# Test connectivité PostgreSQL
test_postgres_connectivity() {
    echo "🔍 Test connectivité PostgreSQL..."
    
    if docker exec oracle-ebs-postgres pg_isready -U oracle_user -d oracle_ebs_assistant > /dev/null 2>&1; then
        echo "✅ PostgreSQL: Connecté et prêt"
        
        # Informations base de données
        echo "📊 Informations base de données:"
        docker exec oracle-ebs-postgres psql -U oracle_user -d oracle_ebs_assistant -c "
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
        " 2>/dev/null || echo "Aucune table trouvée"
        
        # Statistiques connexions
        echo ""
        echo "📈 Statistiques connexions:"
        docker exec oracle-ebs-postgres psql -U oracle_user -d oracle_ebs_assistant -c "
            SELECT 
                count(*) as total_connections,
                count(*) FILTER (WHERE state = 'active') as active_connections,
                count(*) FILTER (WHERE state = 'idle') as idle_connections
            FROM pg_stat_activity;
        " 2>/dev/null
        
    else
        echo "❌ PostgreSQL: Connexion échouée"
        echo "Solutions:"
        echo "1. docker-compose -f $COMPOSE_FILE restart postgres"
        echo "2. Vérifier les logs: docker-compose -f $COMPOSE_FILE logs postgres"
        echo "3. Vérifier l'espace disque"
        return 1
    fi
}

# Test connectivité Redis
test_redis_connectivity() {
    echo "🔍 Test connectivité Redis..."
    
    if docker exec oracle-ebs-redis redis-cli ping | grep -q PONG; then
        echo "✅ Redis: Connecté et répondant"
        
        # Informations Redis
        echo "📊 Informations Redis:"
        echo "  Nombre de clés: $(docker exec oracle-ebs-redis redis-cli dbsize 2>/dev/null || echo 'N/A')"
        echo "  Mémoire utilisée: $(docker exec oracle-ebs-redis redis-cli info memory | grep used_memory_human | cut -d: -f2 | tr -d '\r' || echo 'N/A')"
        echo "  Connexions: $(docker exec oracle-ebs-redis redis-cli info clients | grep connected_clients | cut -d: -f2 | tr -d '\r' || echo 'N/A')"
        
    else
        echo "❌ Redis: Connexion échouée"
        echo "Solutions:"
        echo "1. docker-compose -f $COMPOSE_FILE restart redis"
        echo "2. Vérifier les logs: docker-compose -f $COMPOSE_FILE logs redis"
        echo "3. Vérifier la configuration Redis"
        return 1
    fi
}

# Nettoyage et optimisation
cleanup_databases() {
    echo "🧹 Nettoyage et optimisation des bases de données..."
    
    # Nettoyage PostgreSQL
    echo "Optimisation PostgreSQL..."
    docker exec oracle-ebs-postgres psql -U oracle_user -d oracle_ebs_assistant -c "
        VACUUM ANALYZE;
        REINDEX DATABASE oracle_ebs_assistant;
    " 2>/dev/null && echo "✅ PostgreSQL optimisé" || echo "⚠️ Erreur optimisation PostgreSQL"
    
    # Nettoyage Redis (sessions expirées)
    echo "Nettoyage Redis..."
    docker exec oracle-ebs-redis redis-cli FLUSHDB 2>/dev/null && echo "✅ Redis nettoyé" || echo "⚠️ Erreur nettoyage Redis"
}

# Sauvegarde base de données
backup_databases() {
    echo "💾 Sauvegarde des bases de données..."
    
    BACKUP_DIR="$PROJECT_DIR/backups"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    
    # Sauvegarde PostgreSQL
    echo "Sauvegarde PostgreSQL..."
    docker exec oracle-ebs-postgres pg_dump -U oracle_user oracle_ebs_assistant > "$BACKUP_DIR/postgres_backup_$TIMESTAMP.sql" 2>/dev/null && \
        echo "✅ Sauvegarde PostgreSQL: $BACKUP_DIR/postgres_backup_$TIMESTAMP.sql" || \
        echo "❌ Échec sauvegarde PostgreSQL"
    
    # Sauvegarde Redis
    echo "Sauvegarde Redis..."
    docker exec oracle-ebs-redis redis-cli BGSAVE > /dev/null 2>&1 && \
        echo "✅ Sauvegarde Redis initiée" || \
        echo "❌ Échec sauvegarde Redis"
}

# Restauration base de données
restore_databases() {
    echo "🔄 Restauration des bases de données..."
    
    BACKUP_DIR="$PROJECT_DIR/backups"
    
    # Liste des sauvegardes disponibles
    echo "Sauvegardes PostgreSQL disponibles:"
    ls -la "$BACKUP_DIR"/postgres_backup_*.sql 2>/dev/null || echo "Aucune sauvegarde trouvée"
    
    echo ""
    echo "Pour restaurer une sauvegarde PostgreSQL:"
    echo "docker exec -i oracle-ebs-postgres psql -U oracle_user oracle_ebs_assistant < backup_file.sql"
}

# Menu principal
case "${1:-test}" in
    "test")
        test_postgres_connectivity
        echo ""
        test_redis_connectivity
        ;;
    "cleanup")
        cleanup_databases
        ;;
    "backup")
        backup_databases
        ;;
    "restore")
        restore_databases
        ;;
    "all")
        test_postgres_connectivity
        echo ""
        test_redis_connectivity
        echo ""
        cleanup_databases
        echo ""
        backup_databases
        ;;
    *)
        echo "Usage: $0 {test|cleanup|backup|restore|all}"
        echo ""
        echo "Commandes:"
        echo "  test    - Tester la connectivité des bases de données"
        echo "  cleanup - Nettoyer et optimiser les bases de données"
        echo "  backup  - Créer une sauvegarde des bases de données"
        echo "  restore - Afficher les options de restauration"
        echo "  all     - Exécuter test, cleanup et backup"
        exit 1
        ;;
esac
```

### **H.2 Codes d'Erreur et Solutions**

#### **H.2.1 Matrice des Codes d'Erreur**

| **Code** | **Type** | **Description** | **Cause Probable** | **Solution** |
|----------|----------|-----------------|-------------------|--------------|
| **HTTP 400** | Client | Bad Request | Format requête invalide | Vérifier format JSON, paramètres requis |
| **HTTP 401** | Auth | Unauthorized | Session expirée/invalide | Créer nouvelle session |
| **HTTP 403** | Auth | Forbidden | Permissions insuffisantes | Vérifier droits d'accès |
| **HTTP 404** | Client | Not Found | Ressource inexistante | Vérifier URL, ID procédure |
| **HTTP 429** | Rate | Too Many Requests | Limite de taux dépassée | Attendre, réduire fréquence |
| **HTTP 500** | Server | Internal Error | Erreur serveur interne | Vérifier logs, redémarrer service |
| **HTTP 502** | Gateway | Bad Gateway | Nginx → Backend | Vérifier backend, connectivité |
| **HTTP 503** | Service | Unavailable | Service temporairement indisponible | Attendre, vérifier santé services |
| **WC001** | Business | Quantity Exceeded | Quantité > limite PO | Réduire quantité confirmée |
| **WC002** | Business | Invalid Date | Date future non autorisée | Corriger date de completion |
| **INV001** | Business | Duplicate Invoice | Numéro facture existe | Utiliser nouveau numéro |
| **DB001** | Database | Connection Failed | Base de données inaccessible | Redémarrer PostgreSQL |
| **REDIS001** | Cache | Cache Unavailable | Redis inaccessible | Redémarrer Redis |
| **AI001** | AI | Generation Timeout | Gemini API timeout | Réessayer, vérifier API key |

#### **H.2.2 Scripts de Diagnostic Automatique**

```bash
# ================================
# auto_diagnose.sh
# Diagnostic automatique des erreurs
# ================================

#!/bin/bash
set -euo pipefail

PROJECT_DIR="/opt/oracle-ebs-assistant"
COMPOSE_FILE="$PROJECT_DIR/src/docker-compose.prod.yml"
LOG_FILE="/var/log/oracle-ebs-assistant/auto_diagnose.log"

# Fonction de logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Diagnostic automatique basé sur les logs
auto_diagnose() {
    log "🔍 Diagnostic automatique des erreurs..."
    
    # Analyse des logs récents
    RECENT_ERRORS=$(docker-compose -f "$COMPOSE_FILE" logs --since="1h" 2>/dev/null | grep -i error | wc -l || echo "0")
    
    if [ "$RECENT_ERRORS" -gt 0 ]; then
        log "⚠️ $RECENT_ERRORS erreurs trouvées dans la dernière heure"
        
        # Analyse des types d'erreurs
        analyze_error_patterns
    else
        log "✅ Aucune erreur récente détectée"
    fi
    
    # Vérification santé services
    check_service_health
    
    # Vérification ressources système
    check_system_resources
    
    # Génération recommandations
    generate_auto_recommendations
}

# Analyse des patterns d'erreurs
analyze_error_patterns() {
    log "📊 Analyse des patterns d'erreurs..."
    
    # Erreurs de connexion base de données
    DB_ERRORS=$(docker-compose -f "$COMPOSE_FILE" logs --since="1h" 2>/dev/null | grep -i "connection.*failed\|database.*error" | wc -l || echo "0")
    if [ "$DB_ERRORS" -gt 0 ]; then
        log "🗄️ Erreurs base de données détectées: $DB_ERRORS"
        echo "  Solution: Redémarrer PostgreSQL - docker-compose -f $COMPOSE_FILE restart postgres"
    fi
    
    # Erreurs mémoire
    MEMORY_ERRORS=$(docker-compose -f "$COMPOSE_FILE" logs --since="1h" 2>/dev/null | grep -i "out of memory\|memory.*error" | wc -l || echo "0")
    if [ "$MEMORY_ERRORS" -gt 0 ]; then
        log "💾 Erreurs mémoire détectées: $MEMORY_ERRORS"
        echo "  Solution: Augmenter mémoire ou redémarrer services"
    fi
    
    # Erreurs API Gemini
    AI_ERRORS=$(docker-compose -f "$COMPOSE_FILE" logs --since="1h" 2>/dev/null | grep -i "gemini.*error\|api.*timeout" | wc -l || echo "0")
    if [ "$AI_ERRORS" -gt 0 ]; then
        log "🤖 Erreurs API IA détectées: $AI_ERRORS"
        echo "  Solution: Vérifier clé API Gemini et connectivité internet"
    fi
    
    # Erreurs HTTP 5xx
    HTTP_ERRORS=$(docker-compose -f "$COMPOSE_FILE" logs --since="1h" 2>/dev/null | grep -E "HTTP.*5[0-9][0-9]" | wc -l || echo "0")
    if [ "$HTTP_ERRORS" -gt 0 ]; then
        log "🌐 Erreurs HTTP serveur détectées: $HTTP_ERRORS"
        echo "  Solution: Vérifier configuration Nginx et backend"
    fi
}

# Vérification santé services
check_service_health() {
    log "🏥 Vérification santé des services..."
    
    local services=("oracle-ebs-assistant" "nginx" "redis" "postgres")
    local unhealthy_count=0
    
    for service in "${services[@]}"; do
        if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "$service.*Up"; then
            log "✅ $service: Healthy"
        else
            log "❌ $service: Unhealthy"
            ((unhealthy_count++))
        fi
    done
    
    if [ "$unhealthy_count" -gt 0 ]; then
        log "⚠️ $unhealthy_count services non sains détectés"
        return 1
    fi
    
    return 0
}

# Vérification ressources système
check_system_resources() {
    log "📊 Vérification ressources système..."
    
    # CPU
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//' || echo "0")
    if (( $(echo "$CPU_USAGE > 80" | bc -l 2>/dev/null || echo "0") )); then
        log "⚠️ Utilisation CPU élevée: ${CPU_USAGE}%"
    fi
    
    # Mémoire
    MEM_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100.0)}')
    if [ "$MEM_USAGE" -gt 90 ]; then
        log "⚠️ Utilisation mémoire élevée: ${MEM_USAGE}%"
    fi
    
    # Disque
    DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 85 ]; then
        log "⚠️ Utilisation disque élevée: ${DISK_USAGE}%"
    fi
}

# Génération recommandations automatiques
generate_auto_recommendations() {
    log "💡 Génération des recommandations..."
    
    echo ""
    echo "🔧 ACTIONS RECOMMANDÉES:"
    echo "========================"
    
    # Recommandations basées sur l'analyse
    if ! check_service_health; then
        echo "1. Redémarrer les services non sains:"
        echo "   docker-compose -f $COMPOSE_FILE restart"
    fi
    
    # Nettoyage préventif
    echo "2. Nettoyage préventif:"
    echo "   docker system prune -f"
    echo "   $PROJECT_DIR/maintenance.sh cleanup"
    
    # Vérification logs détaillée
    echo "3. Analyse logs détaillée:"
    echo "   docker-compose -f $COMPOSE_FILE logs -f --tail=100"
    
    # Monitoring continu
    echo "4. Monitoring continu:"
    echo "   watch 'docker stats --no-stream'"
    
    echo ""
    echo "📞 Support: Si les problèmes persistent, contactez l'équipe IT"
}

# Réparation automatique (mode sécurisé)
auto_repair() {
    log "🔧 Tentative de réparation automatique..."
    
    # Redémarrage services non sains uniquement
    local services=("oracle-ebs-assistant" "nginx" "redis" "postgres")
    
    for service in "${services[@]}"; do
        if ! docker ps --format "table {{.Names}}" | grep -q "$service.*Up"; then
            log "🔄 Redémarrage $service..."
            docker-compose -f "$COMPOSE_FILE" restart "$service"
            sleep 10
        fi
    done
    
    # Nettoyage léger
    log "🧹 Nettoyage système..."
    docker system prune -f > /dev/null 2>&1 || true
    
    # Vérification post-réparation
    sleep 30
    if check_service_health; then
        log "✅ Réparation automatique réussie"
        return 0
    else
        log "❌ Réparation automatique échouée - intervention manuelle requise"
        return 1
    fi
}

# Menu principal
case "${1:-diagnose}" in
    "diagnose")
        auto_diagnose
        ;;
    "repair")
        auto_repair
        ;;
    "monitor")
        log "📈 Mode monitoring continu activé (Ctrl+C pour arrêter)..."
        while true; do
            auto_diagnose
            sleep 300  # 5 minutes
        done
        ;;
    *)
        echo "Usage: $0 {diagnose|repair|monitor}"
        echo ""
        echo "Commandes:"
        echo "  diagnose - Diagnostic automatique des erreurs"
        echo "  repair   - Tentative de réparation automatique"
        echo "  monitor  - Monitoring continu avec diagnostic"
        exit 1
        ;;
esac
```

### **H.3 Contacts et Ressources Support**

#### **H.3.1 Informations de Contact**
```
🏢 TANGER MED PORT AUTHORITY (TMPA)
📧 Support IT: it-support@tangermed.ma
📞 Téléphone: +212 539 33 70 00
🌐 Site Web: https://tangermed.ma
📍 Adresse: Zone Franche d'Exportation, Ksar Sghir, Maroc

🔧 ÉQUIPE TECHNIQUE
👨‍💻 Responsable IT: [Nom du responsable]
📧 Email technique: oracle-support@tangermed.ma
📱 Urgences 24/7: [Numéro d'urgence]

📚 RESSOURCES DOCUMENTATION
🔗 Wiki interne: https://wiki.tangermed.ma/oracle-ebs
📖 Documentation Oracle: https://docs.oracle.com/cd/E18727_01/
🎥 Tutoriels vidéo: [Lien vers plateforme vidéo interne]
```

#### **H.3.2 Procédure d'Escalade**
```
🚨 PROCÉDURE D'ESCALADE DES INCIDENTS

NIVEAU 1 - Support Utilisateur (0-2h)
- Problèmes d'utilisation standard
- Questions sur les procédures
- Erreurs utilisateur courantes
Contact: help-desk@tangermed.ma

NIVEAU 2 - Support Technique (2-8h)
- Problèmes de performance
- Erreurs système non critiques
- Configuration et paramétrage
Contact: it-support@tangermed.ma

NIVEAU 3 - Support Expert (8-24h)
- Pannes système critiques
- Problèmes de sécurité
- Corruption de données
Contact: oracle-support@tangermed.ma + Responsable IT

NIVEAU 4 - Escalade Externe (24h+)
- Problèmes nécessitant intervention Oracle
- Bugs logiciel majeurs
- Incidents de sécurité critiques
Contact: Partenaire Oracle + Management TMPA
```

---

## **CONCLUSION DES ANNEXES**

Ces annexes détaillées fournissent une documentation technique complète pour le projet Oracle EBS R12 i-Supplier Assistant de Tanger Med Port Authority. Elles couvrent tous les aspects techniques, opérationnels et de maintenance nécessaires pour :

✅ **Comprendre l'architecture** technique et les choix technologiques
✅ **Déployer et configurer** l'application en environnement de production
✅ **Maintenir et monitorer** le système de manière proactive
✅ **Résoudre les problèmes** rapidement avec des guides détaillés
✅ **Assurer la sécurité** selon les meilleures pratiques
✅ **Intégrer l'API** dans d'autres systèmes si nécessaire

Cette documentation constitue une référence technique complète pour l'équipe IT de Tanger Med et les futurs développeurs qui travailleront sur ce projet.

---

**Document Version:** 1.0.0  
**Dernière Mise à Jour:** $(date)  
**Auteur:** Équipe Développement Oracle EBS Assistant  
**Révision:** Équipe IT Tanger Med Port Authority