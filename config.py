# This file contains all application configurations

# Any configurations placed in this class will be common across all environments
class Config(object):
    """
    Common configurations
    """
# Configurations placed in this class are specifically for the development environment
class DevelopmentConfig(Config):
    DEBUG = True #activates debug mode on the app.
    SQLALCHEMY_ECHO = True # Assists in debugging by allowing SQLAlchemy to log errors.

    # 13/04/2021:
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = True

# Configurations placed in this class are specifically for the production environment
class ProductionConfig(Config):
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}