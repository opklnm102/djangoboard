from django.conf.urls import url

from user_manager.views import login, login_validate

urlpatterns = [
    url(r'^login/$', login),
    # ^ - 시작, $ - 끝 --> login/으로 시작하고, validate/로 끝나는
    url(r'^login/validate/$', login_validate),
]
