# 自定义中间类
from django.utils.deprecation import MiddlewareMixin


class Md1(MiddlewareMixin):
    def process_request(self, request):
        print('process_request')

    def process_response(self, request, response):
        print('process_response')
        return response
