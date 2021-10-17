from flask import Blueprint
from flask_restful import Api

api_blueprint = Blueprint('api', __name__)

from .resource import account, home

api = Api()
api.init_app(api_blueprint)

# 路由资源
api.add_resource(account.RegisterView, "/register", endpoint="register")
api.add_resource(account.LoginView, "/login", endpoint="login")
api.add_resource(account.ModifyPassWord, "/mPassword", endpoint="mPassword")
api.add_resource(account.AddCategory, "/blogCategory", endpoint="blogCategory")
api.add_resource(home.BlogListView, "/blog", endpoint="blogList")
api.add_resource(home.BlogDetailView, "/blog/<int:id>", endpoint="blogDetail")
