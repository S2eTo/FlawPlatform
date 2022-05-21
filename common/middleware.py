import re

from django.conf import settings
from django.http.request import (
    split_domain_port, validate_host
)
from django.core.exceptions import DisallowedHost
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.middleware import SessionMiddleware


class CorsHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        """
        处理跨域响应头
        """

        response['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
        response['Access-Control-Max-Age'] = 'POST,GET,OPTIONS'
        response['Access-Control-Allow-Headers'] = 'content-type,x-token'
        response['Access-Control-Allow-Origin'] = '*'
        return response


class RestFulSessionMiddleware(SessionMiddleware):
    """
    前后端分离重写 Django 默认身份验证
    """

    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        if session_key is None:
            # 如请求头中传入的参数为：X-Token 实际上会被转成 HTTP_X_TOKEN
            session_key = request.META.get("HTTP_X_TOKEN")
            request.session = self.SessionStore(session_key)


class RestFulCsrfViewMiddleware(MiddlewareMixin):
    """
    API 不设 CSRF 校验
    """

    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        if session_key is None:
            setattr(request, '_dont_enforce_csrf_checks', True)
