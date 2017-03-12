from rest_framework import serializers

from post_service.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at')
