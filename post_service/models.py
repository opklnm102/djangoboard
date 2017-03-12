from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=1024)
    content = models.CharField(max_length=4096)
    author = models.ForeignKey(User)

    # 현재시간으로 자동 생성
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
