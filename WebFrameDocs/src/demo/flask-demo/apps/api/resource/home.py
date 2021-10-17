import json
from datetime import datetime
from json import JSONDecodeError

from flask import request

from apps import db
from apps.api.common.response import response
from apps.api.resource.Base import BaseView
from apps.models import Note, Category


class BlogListView(BaseView):

    def get(self, *args, **kwargs):
        # 获取博客列表
        all_note = Note.query.all()
        note = []
        for c in all_note:
            note.append({"id": c.id, "title": c.title})
        return response(200, "获取成功", note)

    @BaseView.auth
    def post(self, *args, **kwargs):
        # 添加博客

        try:
            _ = json.loads(request.get_data())
            category = _.get('category')
            content = _.get('content')
            title = _.get('title')
            top_image = _.get("top_image")
        except JSONDecodeError:
            return response(400, "数据格式异常")

        if not all([category, title, content]):
            return response(400, "数据不完整")

        category = Category.query.filter_by(name=category).first()
        if not category:
            return response(400, "分类不存在")

        note = Note.query.filter_by(title=title).first()
        if note:
            return response(400, "请不要重复添加")

        _note = Note(user_id=kwargs["user"].id,
                     category_id=category.id,
                     title=title,
                     content=content,
                     modify_datetime=datetime.now(),
                     top_image=top_image)

        db.session.add(_note)
        db.session.commit()

        return response(200, "添加成功", {
            "categoryId": _note.id,
            "category": _note.category.name,
            "titleId": _note.id,
            "title": _note.title,
            "content": _note.content,
            "top_image": _note.top_image
        })


class BlogDetailView(BaseView):

    def get(self, *args, **kwargs):
        # 获取单条博客
        id = kwargs.get("id", None)
        note = Note.query.filter_by(id=id).first()
        if note:
            return response(200, "获取成功", {
                "categoryId": note.id,
                "category": note.category.name,
                "titleId": note.id,
                "title": note.title,
                "content": note.content,
                "top_image": note.top_image
            })
        else:
            return response(200, "数据不存在")

    @BaseView.auth
    def put(self, *args, **kwargs):
        # 修改博客

        id = kwargs.get("id", None)

        try:
            _ = json.loads(request.get_data())
            category = _.get('category')
            content = _.get('content')
            title = _.get('title')
            top_image = _.get("top_image")
        except JSONDecodeError:
            return response(400, "数据格式异常")

        note = Note.query.filter_by(id=id).first()
        if not note:
            return response(400, "博客不存在")

        category = Category.query.filter_by(name=category).first()
        if not category:
            return response(400, "分类不存在")

        note.category_id = category.id
        note.title = title
        note.content = content
        note.top_image = top_image

        db.session.add(note)
        db.session.commit()

        return response(200, "修改成功", {
            "categoryId": note.id,
            "category": note.category.name,
            "titleId": note.id,
            "title": note.title,
            "content": note.content,
            "top_image": note.top_image
        })

    @BaseView.auth
    def delete(self, *args, **kwargs):
        # 删除博客

        id = kwargs.get("id", None)

        Note.query.filter_by(id=id).delete()
        db.session.commit()
        return response(200, "删除成功")
