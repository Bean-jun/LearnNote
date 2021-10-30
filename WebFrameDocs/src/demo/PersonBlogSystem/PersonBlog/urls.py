"""PersonBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.blog.urls', namespace='blog')),  # 博客系统
    path('oauth/', include('apps.oauth.urls', namespace='auth')),  # 博客系统
    path('service/', include('apps.web.urls', namespace='service')),  # SaaS系统
    path('api/<str:version>/', include('apps.api.urls', namespace='api')),

    # V1版本api
    # path('v1/', include(
    # ([
    #     path('api/', include('api.urls')),  # api
    #     path('api/docs/', include_docs_urls(title="接口文档")),
    # ])
    # )),
]
