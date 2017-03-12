from django.conf.urls import url

from user_manager.views import login_page, login_validate, join_page

urlpatterns = [
    url(r'^login/$', login_page),
    # ^ - 시작, $ - 끝 --> login/으로 시작하고, validate/로 끝나는
    url(r'^login/validate/$', login_validate),
    url(r'join/$', join_page),
]
