"""
Configurations for the Flask app. 
"""

class Config:
    DATABASE = "app.db"
    DEBUG = False

class DevConfig(Config):
    DEBUG = True