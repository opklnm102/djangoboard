from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.template import Context
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from post_service.models import Post
from post_service.serializers import PostSerializer


# GenericAPIView는 다른 Mixin클래스와의 조합으로 쉽고 빠르게 구현하는 방법 제공
# ListModelMixin - queryset, serializer_class기반으로 data list생성,
class blog_api(GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all().order_by('-created_at')  # 어떤 모델읇 보여줄 것인가
    serializer_class = PostSerializer

    # rest_framework는 request, *args, **kwargs를 반드시 포함해서 처리하게 되어있다
    def get(self, request, *args, **kwargs):
        # 요청에 대한 Parsing작업을 하여 request생성, 그외 데이터는 *args, **kwargs에 포함
        return self.list(request, *args, **kwargs)


def post_list(request):
    page_data = Paginator(Post.objects.all().order_by('-created_at'), 2)
    page = request.GET.get('page')
    try:
        posts = page_data.page(page)
    except PageNotAnInteger:
        posts = page_data.page(1)
        page = 1
    except EmptyPage:
        posts = page_data.page(page_data.num_pages)  # total count
        page =page_data.num_pages

    context = Context({'posts': posts,
                       'current_page': int(page),
                       'total_page': range(1, page_data.num_pages + 1)  # 0부터 시작해서 +1
                       })

    return render(request, 'post_service/post_list.html', context)
