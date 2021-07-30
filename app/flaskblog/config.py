class Config:
    SECRET_KEY = '094a93556eb2e0c417273ace49742a89'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'vishnumanoharan2k@gmail.com'
    MAIL_PASSWORD = "asdfasdf"