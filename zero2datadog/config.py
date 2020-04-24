import os
import ddtrace
basedir = os.path.abspath(os.path.dirname(__file__))

ddtrace.config.analytics_enabled = True
ddtrace.config.flask['service_name'] = "zero2datadog"

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SUPER-SECRET'
    LOGFILE = "/var/log/python/python.log"

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_BACKTRACE = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    LOG_BACKTRACE = False
    LOG_LEVEL = 'INFO'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

