""" system info
本视图用于单片机和服务器的通行

SystemInfo视图中
    - get请求适用于机器获取数据
    - post请求适用于单片机向后台提交的数据信息
"""

from datetime import datetime, timedelta

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.auth.auth import LoginParamAuthentication
from apps.api.models import VisitorRecord, CityWeather
from apps.api.serializer.machine import MachineSerializer
from apps.blog.models import Note
from utils.weather import get_weather


class SystemInfo(APIView):
    """系统信息"""

    authentication_classes = [LoginParamAuthentication, ]

    def get(self, request, *args, **kwargs):
        """机器获取数据"""
        if request.user.email in settings.ADMIN_ACCOUNT:

            # 处理文章数量统计，访问统计，xxx
            count = Note.objects.all().count()
            visitor_count = VisitorRecord.objects.all().count()
            visitor_list = VisitorRecord.objects.all().order_by("-create_datetime").values_list('addr', 'host')[:3]

            # 获取天气信息
            weather_data = {
                "status": False
            }
            weather = CityWeather.objects.order_by('-create_datetime').first()

            if weather is not None:
                # 比较时间，时间太短不需要爬取，直接查询数据库即可
                if weather.create_datetime + timedelta(hours=1) > datetime.now():
                    # 查询数据库
                    weather_data["status"] = True

            if weather_data["status"] is False:
                # 爬取最新数据
                addr = request.query_params.get("addr", "武汉")
                data = get_weather(addr)

                weather = CityWeather.objects.create(city=addr,
                                                     city_num=data['city'],
                                                     temperature=data['temp'],
                                                     humidity=data["SD"],
                                                     wind=data["WD"] + data["WS"],
                                                     aqi=data["aqi"])

            weather_data["status"] = True
            weather_data["city"] = weather.city
            weather_data["temperature"] = weather.temperature
            weather_data["humidity"] = weather.humidity
            weather_data["wind"] = weather.wind
            weather_data["aqi"] = weather.aqi

            data = {
                "文章数量": count,
                "访问数量": visitor_count,
                "访问记录": visitor_list,
                "天气情况": weather_data
            }
            return Response({"msg": data, "status": True})
        else:
            return Response({"msg": "请使用管理员账号", "status": False})

    def post(self, request, *args, **kwargs):
        """接受机器数据"""
        # print(request.data)

        if request.user.email in settings.ADMIN_ACCOUNT:

            serializer = MachineSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"msg": serializer.data, "status": True})
            return Response({"msg": "数据格式错误", "status": False})
        else:
            return Response({"msg": "请使用管理员账号", "status": False})
