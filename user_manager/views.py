from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from user_manager.forms import LoginForm


def login(request):
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
