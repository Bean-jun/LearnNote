class Config(object):
    '''基本配置'''
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'abc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 管理员
    SUPER_USER = ["xxx@gmail.com"]  

    # 头像目录
    UPLOAD_FOLDER = "xxxx"
    # 默认注册默认头像
    USER_LOGO = "xxxx"

    # top_image目录
    TOP_IMAGE_UPLOAD_FOLDER = "xxxx"

    # token 过期时间 (单位：秒)
    TOKEN_EXP = 60 * 60


class DevelopConfig(Config):
    '''开发环境'''
    TESTING = False


class ProductConfig(Config):
    '''生产环境'''
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    '''测试环境'''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# 配置图
ConfigMap = {
    'develop': DevelopConfig,
    'product': ProductConfig,
    'test': TestConfig,
}
