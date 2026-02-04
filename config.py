"""
Configuration Module

This module contains configuration settings for the PDF Downloader and Parser application.
"""

import os
import sys


class Config:
    """
    Base configuration class for the application.
    """
    # Application settings
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Directory settings
    DOWNLOAD_DIR = os.environ.get('DOWNLOAD_DIR', 'downloads')
    OUTPUT_DIR = os.environ.get('OUTPUT_DIR', 'output')
    
    # Download settings
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 30))
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 50 * 1024 * 1024))  # 50 MB default
    
    # Parser settings
    SUPPORTED_ANSWER_PATTERNS = [
        r'Q(\d+)[:\s]+([A-D])',  # Q1: A format
        r'(\d+)\.\s*([A-D])\b',  # 1. A format
        r'(\d+)\)\s*([A-D])\b',  # 1) A format
        r'Question\s+(\d+)[:\s]+([A-D])',  # Question 1: A format
        r'^\s*(\d+)\s+([A-D])\s*$',  # 1 A format
    ]
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        if os.environ.get('FLASK_ENV') == 'production':
            print("ERROR: SECRET_KEY must be set in production!", file=sys.stderr)
            sys.exit(1)
        else:
            SECRET_KEY = 'dev-secret-key-change-in-production'
    
    MAX_CONTENT_LENGTH = MAX_FILE_SIZE


class DevelopmentConfig(Config):
    """
    Development configuration.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configuration.
    """
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
