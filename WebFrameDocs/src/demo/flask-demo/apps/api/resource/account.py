import json
from json import JSONDecodeError

from flask import request, current_app
from sqlalchemy import or_

from apps import db
from apps.api.common.response import response
from apps.api.resource.Base import BaseView
from apps.models import UserInfo, Category, Note


class RegisterView(BaseView):

    def post(self):
        try:
            _ = json.loads(request.get_data())
            username = _.get('username')
            email = _.get('email')
            pwd = _.get('pwd')
            confirm_pwd = _.get('confirm_pwd')
        except JSONDecodeError:
            return response(400, "数据格式异常")

        if not all([username, email, pwd, confirm_pwd]):
            return response(400, "请输入完整的账号及密码")

        if pwd != confirm_pwd:
            return response(400, "请确保密码一致")

        user = UserInfo.query.filter_by(email=email).first()
        if user:
            return response(400, "此账号已经注册")

        user = UserInfo(username=username, email=email)

        if email in current_app.config['SUPER_USER']:
            user.is_super = True
        else:
            user.is_super = False

        user.password = pwd
        db.session.add(user)
        db.session.commit()

        return response(200, "注册成功", {"username": user.username, "token": self.token_encode(
            username=user.username,
            email=user.email
        )})


class LoginView(BaseView):

    def post(self):
        try:
            _ = json.loads(request.get_data())
            username = _.get('username')
            pwd = _.get('pwd')
        except JSONDecodeError:
            return response(400, "数据格式异常")

        if not all([username, pwd]):
            return response(400, "账号信息不完整")

        user = UserInfo.query.filter(or_(UserInfo.username == username, UserInfo.email == username)).first()
        if not user:
            return response(400, "账号不存在")

        if not user.check_password(pwd):
            return response(400, "账号密码有误")

        return response(200, "登录成功", {"username": user.username, "token": self.token_encode(
            username=user.username,
            email=user.email
        )})


class ModifyPassWord(BaseView):

    def post(self):
        try:
            _ = json.loads(request.get_data())
            username = _.get('username')
            old_pwd = _.get("old_pwd")
            pwd = _.get('pwd')
            confirm_pwd = _.get('confirm_pwd')
        except JSONDecodeError:
            return response(400, "数据格式异常")

        if not all([username, old_pwd, pwd, confirm_pwd]):
            return response(400, "信息不完整")

        if pwd != confirm_pwd:
            return response(400, "新密码不一致")

        user = UserInfo.query.filter(or_(UserInfo.username == username, UserInfo.email == username)).first()
        if not user:
            return response(400, "账号不存在")

        if not user.check_password(old_pwd):
            return response(400, "账号密码有误")

        if user.check_password(pwd):
            return response(400, "新密码不得与旧密码一致")

        user.password = pwd
        db.session.add(user)
        db.session.commit()

        return response(200, "修改成功", {"username": user.username, "token": self.token_encode(
            username=user.username,
            email=user.email
        )})


class AddCategory(BaseView):

    def get(self, *args, **kwargs):
        all_category = Category.query.all()
        category = []
        for c in all_category:
            category.append({"id": c.id, "name": c.name})
        return response(200, "获取成功", category)

    @BaseView.auth
    def post(self, *args, **kwargs):

        try:
            _ = json.loads(request.get_data())
            category = _.get('category')
        except JSONDecodeError:
            return response(400, "数据格式异常")

        exist = Category.query.filter_by(name=category).first()
        if exist:
            return response(400, "请勿重复添加")

        category = Category(user_id=kwargs["user"].id,
                            name=category)

        db.session.add(category)
        db.session.commit()

        return response(200, "添加成功", {"categoryId": category.id, "category": category.name})

    @BaseView.auth
    def delete(self, *args, **kwargs):

        try:
            _ = json.loads(request.get_data())
            category = _.get('category')
        except JSONDecodeError:
            return response(400, "数据格式异常")

        category = Category.query.filter_by(name=category).first()
        if not category:
            return response(200, "数据不存在")

        # 删除该分类对应的note
        Note.query.filter_by(category_id=category.id).delete()

        db.session.delete(category)
        db.session.commit()

        return response(200, "删除成功")
