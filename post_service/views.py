from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from post_service.forms import LoginForm
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

    if page is None:
        page = 1

    try:
        posts = page_data.page(page)
    except PageNotAnInteger:
        posts = page_data.page(1)
    except EmptyPage:
        posts = page_data.page(page_data.num_pages)  # total count

    context = Context({'posts': posts,
                       'current_page': int(page),
                       'total_page': range(1, page_data.num_pages + 1)  # 0부터 시작해서 +1
                       })

    return render(request, 'post_service/post_list.html', context)


def login(request):
    context = Context({'login_form': LoginForm()})
    # context.update(csrf(request))  # csrf token refresh

    return render(request, 'post_service/login_form.html', context)


# login 처리
def login_validate(request):
    login_form_data = LoginForm(request.POST)

    if login_form_data.is_valid():
        # form이 정의한 내용과 일치 -> 로그인 시도
        # authenticate()는 username, password등으로 인증과정 수행
        user = auth.authenticate(username=login_form_data.cleaned_data['id'], password=login_form_data.cleaned_data['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)

                return redirect('/board')
        else:
            return HttpResponse('사용자가 없거나 비밀번호를 잘못 누르셨습니다.')
    else:
        return HttpResponse('로그인 폼이 비정상적입니다.')

    return HttpResponse('알 수 없는 오류입니다.')
