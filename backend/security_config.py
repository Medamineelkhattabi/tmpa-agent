"""Security configuration for Oracle EBS Assistant"""

import os
from typing import List

# Environment-based security settings
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    'requests_per_minute': int(os.getenv('RATE_LIMIT_PER_MINUTE', '60')),
    'requests_per_hour': int(os.getenv('RATE_LIMIT_PER_HOUR', '1000')),
    'burst_limit': int(os.getenv('RATE_LIMIT_BURST', '10')),
    'lockout_duration_minutes': int(os.getenv('LOCKOUT_DURATION', '15'))
}

# Input validation limits
INPUT_LIMITS = {
    'max_message_length': int(os.getenv('MAX_MESSAGE_LENGTH', '5000')),
    'max_session_duration_hours': int(os.getenv('MAX_SESSION_DURATION', '24')),
    'max_failed_attempts': int(os.getenv('MAX_FAILED_ATTEMPTS', '5'))
}

# Allowed hosts for production
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*.tangermed.ma',
    '*.tanger-med.com'
]

# CORS origins based on environment
if ENVIRONMENT == 'production':
    CORS_ORIGINS = [
        'https://ebs.tangermed.ma',
        'https://supplier.tangermed.ma'
    ]
else:
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000'
    ]

# Security headers configuration
SECURITY_HEADERS_CONFIG = {
    'production': {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
        'Content-Security-Policy': (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://ebs.tangermed.ma; "
            "frame-ancestors 'none'; "
            "base-uri 'self';"
        )
    },
    'development': {
        'Content-Security-Policy': (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' http://localhost:8000; "
            "frame-ancestors 'none';"
        )
    }
}

# Blocked file extensions for uploads
BLOCKED_EXTENSIONS = [
    '.exe', '.bat', '.cmd', '.com', '.pif', '.scr', '.vbs', '.js', '.jar',
    '.php', '.asp', '.aspx', '.jsp', '.py', '.rb', '.pl', '.sh', '.ps1'
]

# Monitoring and alerting thresholds
SECURITY_THRESHOLDS = {
    'failed_attempts_per_ip': 10,
    'suspicious_patterns_per_hour': 5,
    'rate_limit_violations_per_hour': 20,
    'error_rate_threshold': 0.1  # 10% error rate
}

# Logging configuration
SECURITY_LOGGING = {
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    'log_file': os.getenv('SECURITY_LOG_FILE', 'security.log'),
    'max_log_size_mb': int(os.getenv('MAX_LOG_SIZE_MB', '100')),
    'backup_count': int(os.getenv('LOG_BACKUP_COUNT', '5'))
}