import os

class Config:
        SECRET_KEY = os.environ.get("secret_key_")
        SQLALCHEMY_DATABASE_URI = os.environ.get("database_urI_")
        MAIL_SERVER = 'smtp.gmail.com' 
        MAIL_PORT = 465
        MAIL_USE_TLS = False
        MAIL_USE_SSL = True
        MAIL_USERNAME = os.environ.get("email_d_")
        MAIL_PASSWORD = os.environ.get("pass_d_")