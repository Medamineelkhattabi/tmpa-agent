import re
import time
import hashlib
import secrets
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from collections import defaultdict
import html
import bleach

class SecurityManager:
    """Comprehensive security manager for Oracle EBS Assistant"""
    
    def __init__(self):
        # Rate limiting
        self.request_counts = defaultdict(list)
        self.blocked_ips = set()
        self.max_requests_per_minute = 60
        self.max_requests_per_hour = 1000
        
        # Input validation
        self.max_message_length = 5000
        self.blocked_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'eval\s*\(',
            r'document\.',
            r'window\.',
            r'alert\s*\(',
            r'prompt\s*\(',
            r'confirm\s*\(',
            r'<iframe',
            r'<object',
            r'<embed',
            r'<link',
            r'<meta',
            r'<style',
            r'vbscript:',
            r'data:text/html',
            r'expression\s*\(',
            r'@import',
            r'url\s*\(',
            r'<\s*\/?\s*(script|iframe|object|embed|link|meta|style|form|input)',
        ]
        
        # SQL injection patterns
        self.sql_patterns = [
            r'union\s+select',
            r'drop\s+table',
            r'delete\s+from',
            r'insert\s+into',
            r'update\s+set',
            r'exec\s*\(',
            r'sp_\w+',
            r'xp_\w+',
            r'--\s*$',
            r'/\*.*?\*/',
            r';\s*drop',
            r';\s*delete',
            r';\s*insert',
            r';\s*update',
            r'0x[0-9a-f]+',
            r'char\s*\(',
            r'ascii\s*\(',
            r'substring\s*\(',
            r'waitfor\s+delay',
        ]
        
        # Session security
        self.session_tokens = {}
        self.failed_attempts = defaultdict(int)
        self.lockout_duration = timedelta(minutes=15)
        self.max_failed_attempts = 5
        
    def validate_input(self, message: str, client_ip: str) -> Dict[str, any]:
        """Comprehensive input validation"""
        
        # Check rate limiting
        if not self.check_rate_limit(client_ip):
            return {"valid": False, "error": "Rate limit exceeded", "block": True}
        
        # Check if IP is blocked
        if client_ip in self.blocked_ips:
            return {"valid": False, "error": "IP blocked", "block": True}
        
        # Length validation
        if len(message) > self.max_message_length:
            return {"valid": False, "error": "Message too long"}
        
        # Sanitize and validate content
        sanitized_message = self.sanitize_input(message)
        
        # Check for malicious patterns
        threat_detected = self.detect_threats(message.lower())
        if threat_detected:
            self.log_security_event(client_ip, "threat_detected", threat_detected)
            return {"valid": False, "error": "Potentially malicious content detected"}
        
        return {"valid": True, "sanitized_message": sanitized_message}
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize user input"""
        # HTML escape
        text = html.escape(text)
        
        # Use bleach for additional sanitization
        allowed_tags = []  # No HTML tags allowed
        text = bleach.clean(text, tags=allowed_tags, strip=True)
        
        # Remove null bytes and control characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()
    
    def detect_threats(self, text: str) -> Optional[str]:
        """Detect various security threats"""
        
        # XSS detection
        for pattern in self.blocked_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return f"XSS_PATTERN: {pattern}"
        
        # SQL injection detection
        for pattern in self.sql_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return f"SQL_INJECTION: {pattern}"
        
        # Command injection detection
        cmd_patterns = [
            r';\s*(rm|del|format|shutdown|reboot)',
            r'\|\s*(nc|netcat|wget|curl)',
            r'`[^`]*`',
            r'\$\([^)]*\)',
            r'&&\s*(rm|del|format)',
        ]
        
        for pattern in cmd_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return f"COMMAND_INJECTION: {pattern}"
        
        # Path traversal detection
        if re.search(r'\.\.[\\/]', text):
            return "PATH_TRAVERSAL"
        
        return None
    
    def check_rate_limit(self, client_ip: str) -> bool:
        """Check if client exceeds rate limits"""
        current_time = time.time()
        
        # Clean old requests
        self.request_counts[client_ip] = [
            req_time for req_time in self.request_counts[client_ip]
            if current_time - req_time < 3600  # Keep last hour
        ]
        
        # Add current request
        self.request_counts[client_ip].append(current_time)
        
        # Check limits
        recent_requests = [
            req_time for req_time in self.request_counts[client_ip]
            if current_time - req_time < 60  # Last minute
        ]
        
        if len(recent_requests) > self.max_requests_per_minute:
            self.block_ip(client_ip, "Rate limit exceeded (per minute)")
            return False
        
        if len(self.request_counts[client_ip]) > self.max_requests_per_hour:
            self.block_ip(client_ip, "Rate limit exceeded (per hour)")
            return False
        
        return True
    
    def block_ip(self, client_ip: str, reason: str):
        """Block an IP address"""
        self.blocked_ips.add(client_ip)
        self.log_security_event(client_ip, "ip_blocked", reason)
    
    def generate_session_token(self, session_id: str) -> str:
        """Generate secure session token"""
        token = secrets.token_urlsafe(32)
        self.session_tokens[session_id] = {
            'token': token,
            'created': datetime.now(),
            'last_used': datetime.now()
        }
        return token
    
    def validate_session_token(self, session_id: str, token: str) -> bool:
        """Validate session token"""
        if session_id not in self.session_tokens:
            return False
        
        stored_token = self.session_tokens[session_id]
        
        # Check token match
        if not secrets.compare_digest(stored_token['token'], token):
            return False
        
        # Check expiration (24 hours)
        if datetime.now() - stored_token['created'] > timedelta(hours=24):
            del self.session_tokens[session_id]
            return False
        
        # Update last used
        stored_token['last_used'] = datetime.now()
        return True
    
    def log_security_event(self, client_ip: str, event_type: str, details: str):
        """Log security events"""
        timestamp = datetime.now().isoformat()
        print(f"[SECURITY] {timestamp} - IP: {client_ip} - Event: {event_type} - Details: {details}")
    
    def get_client_ip(self, request) -> str:
        """Extract client IP from request"""
        # Check for forwarded headers
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        
        real_ip = request.headers.get('X-Real-IP')
        if real_ip:
            return real_ip
        
        return request.client.host if hasattr(request, 'client') else '127.0.0.1'

# Content Security Policy
CSP_POLICY = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
    "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
    "img-src 'self' data: https:; "
    "connect-src 'self' http://localhost:8000; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self';"
)

# Security headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Content-Security-Policy": CSP_POLICY
}