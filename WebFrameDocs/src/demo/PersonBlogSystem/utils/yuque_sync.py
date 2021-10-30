import json
import requests


class YuQueConnect:
    """语雀数据获取及推送"""

    def __init__(self, token, headers):
        """
        token: 获取token
        headers: 请求头
        """
        self.BASE_URL = "https://www.yuque.com/api/v2/"
        self.token = token
        self.headers = headers

    def _request(self, method, path, **kwargs):
        try:
            self.headers['X-Auth-Token'] = self.token
            if isinstance(method, str):
                response = requests.request(method.upper(), self.BASE_URL + path, data=json.dumps(kwargs),
                                            headers=self.headers)
            else:
                raise Exception("error")
        except Exception as e:
            raise e

        return response

    def get(self, path):
        """
        获取数据
        path: 路径资源
        """
        response = self._request('get', path)
        return response.json()

    def post(self, path, **kwargs):
        """
        发送数据
        path: 路径资源
        data: 发送数据
        """
        response = self._request('post', path, **kwargs)
        return response.json()

    def put(self, path, **kwargs):
        """
        更新数据
        path: 路径资源
        data: 发送数据
        """
        response = self._request('put', path, **kwargs)
        return response.json()

    def delete(self, path):
        """
        更新数据
        path: 路径资源
        data: 发送数据
        """
        response = self._request('delete', path)
        return response.json()

    def _get_user_id(self):
        # 获取用户ID
        res = self.get('user')
        return res['data']['login']

    def get_user_repos(self):
        """
        获取某个用户的知识库列表
        """
        user_id = self._get_user_id()
        path = 'users/{}/repos'.format(user_id)
        response = self.get(path)
        return response

    def create_user_repos(self, **kwargs):
        """
        创建某个用户的知识库

        name    string  仓库名称
        slug    string  slug
        description string  说明
        public  integer
                            0 私密,
                            1 所有人可见,
                            2 空间成员可见，
                            3 空间所有人（含外部联系人）可见
                            4 知识库成员可见
        type    string  ‘Book’ 文库, ‘Design’ 画板, 请注意大小写
        """
        user_id = self._get_user_id()
        path = 'users/{}/repos'.format(user_id)
        response = self.post(path, **kwargs)
        return response

    def drop_user_repos(self, repos_slug):
        """
        删除一个知识库
        repos_slug: 知识库标记
        """
        user_id = self._get_user_id()
        path = 'repos/{}/{}'.format(user_id, repos_slug)
        response = self.delete(path)
        return response

    def get_repos_list_docs(self, repos_slug):
        """
        获取一个仓库的文档列表
        repos_slug: 知识库标记
        """
        user_id = self._get_user_id()
        path = 'repos/{}/{}/docs'.format(user_id, repos_slug)
        response = self.get(path)
        return response

    def get_repos_docs(self, repos_slug, slug):
        """
        获取一个仓库的文档列表
        repos_slug： 知识库标记
        slug: 文章标记
        """
        user_id = self._get_user_id()
        path = 'repos/{}/{}/docs/{}'.format(user_id, repos_slug, slug)
        response = self.get(path)
        return response

    def create_docs(self, repos_slug, **kwargs):
        """
        创建文章
        repos_slug： 知识库标记

        title   标题
        slug    文档 Slug
        public  0 - 私密，1 - 公开
        format  支持 markdown 和 lake，默认为 markdown
        body    format 描述的正文内容，最大允许 5MB
        """
        user_id = self._get_user_id()
        path = 'repos/{}/{}/docs/'.format(user_id, repos_slug)
        response = self.post(path, **kwargs)
        return response

    def update_docs(self, repos_slug, id, **kwargs):
        """
        更新文章
        repos_slug： 知识库标记
        id: 文章当前id

        title   标题
        slug    文档 Slug
        public  0 - 私密，1 - 公开
        body    format 描述的正文内容，最大允许 5MB
        """
        user_id = self._get_user_id()
        path = 'repos/{}/{}/docs/{}'.format(user_id, repos_slug, id)
        response = self.put(path, **kwargs)
        return response


if __name__ == "__main__":
    client = YuQueConnect('xxx', 'xxx')
    # 创建知识库测试
    detail = {
        "name": "张三",
        "slug": "zhangsan",
        "description": "没有",
        "public": 0,
        "type": "Book"
    }
    res = client.drop_user_repos("zhangsan")
    res = client.create_user_repos(**detail)
    blog_detail = {
        "title": "张三",
        "slug": "zhangsan01",
        "public": 0,
        "body": """# 基本文档""",
    }
    update_blog_detail = {
        "title": "张三-更新",
        "slug": "zhangsan01",
        "public": 0,
        "body": """# 基本文档""",
    }

    client.create_docs('zhangsan', **blog_detail)
    client.update_docs('zhangsan', 45408289, **update_blog_detail)
