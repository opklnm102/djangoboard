from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from user_manager.forms import LoginForm, JoinForm


def login_page(request):
    context = Context({'login_form': LoginForm()})
    # context.update(csrf(request))  # csrf token refresh

    return render(request, 'user_manager/login_form.html', context)


# login 처리
def login_validate(request):
    login_form_data = LoginForm(request.POST)

    if login_form_data.is_valid():
        # form이 정의한 내용과 일치 -> 로그인 시도
        # authenticate()는 username, password등으로 인증과정 수행
        user = auth.authenticate(username=login_form_data.cleaned_data['id'],
                                 password=login_form_data.cleaned_data['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)

                return redirect('/board')
        else:
            return HttpResponse('사용자가 없거나 비밀번호를 잘못 누르셨습니다.')
    else:
        return HttpResponse('로그인 폼이 비정상적입니다.')

    return HttpResponse('알 수 없는 오류입니다.')


def join_page(request):
    # POST로 넘어온 데이터에 대해서만 회원가입
    if request.method == 'POST':
        form_data = JoinForm(request.POST)

        if form_data.is_valid():
            username = form_data.cleaned_data['id']
            password = form_data.cleaned_data['password']
            User.objects.create_user(username=username, password=password)

            return redirect('/user/login')
    else:
        # GET이면 빈 FORM 생성
        form_data = JoinForm()

    context = Context({'join_form': form_data})
    return render(request, 'user_manager/join_form.html', context)
