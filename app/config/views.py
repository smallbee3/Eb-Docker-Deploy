from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()


def index(request):
    # 모든 유저의 username, img_profile, nickname을 리스트(ul > li)로
    # 보여주는 뷰 생성
    # 이 뷰에는 새 CSS를 적용 (BootStrap, static/bootstrap/css/bootstrap.css)를 템플릿에 static태그로

    user_list = User.objects.all()

    context = {
        'user_list': user_list
    }
    return render(request, 'index.html', context)
