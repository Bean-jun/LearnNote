from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from apps import db


class UserInfo(db.Model):
    """用户表"""
    __tablename__ = "userinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    _password = db.Column(db.String(32), nullable=False)
    is_super = db.Column(db.BOOLEAN, default=False)  # 是否为管理员
    image = db.Column(db.String(256))  # 用户头像
    create_datetime = db.Column(db.DATETIME, default=datetime.now)

    category = db.relationship('Category', backref="user")  # 用户的文章分类
    note = db.relationship('Note', backref="user")  # 用户的文章
 
    def __repr__(self):
        return self.username

    @property
    def password(self):
        raise AttributeError("密码不可读")

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, pwd):
        return check_password_hash(self._password, pwd)


class Category(db.Model):
    """分类表"""
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("userinfo.id"))
    name = db.Column(db.String(32), nullable=False)
    create_datetime = db.Column(db.DATETIME, default=datetime.now)

    note = db.relationship('Note', backref="category")  # 用户的评论

    def __repr__(self):
        return self.name


class Note(db.Model):
    """用户笔记表"""
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("userinfo.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    title = db.Column(db.String(32), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    create_datetime = db.Column(db.DATETIME, default=datetime.now)
    modify_datetime = db.Column(db.DATETIME, nullable=False)
    top_image = db.Column(db.String(256))
