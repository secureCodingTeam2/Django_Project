from django.shortcuts import render, redirect
from django.db import connection
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from board.models import board

from datetime import date


# Create your views here.

def index(request):
    rows=board.objects.all().order_by('-id')
    search=''

    if request.method == 'POST': #검색을 시도할 경우 POST로 요청이 들어옴
        search=request.POST.get('search')

        if search:
            rows= board.objects.filter(title__iexact=search) #filter함수를 통해 원하는 값을 가져옴
                                                            #title__iexact : DB에 title을 기준으로 대소문자 구분 없이 문자열이 완전히 일치하는 값을 가져옴


    paginator = Paginator(rows, 4)  # 페이지네이션을 위한 객체 생성, 파라미터로는 값과 한 페이지에 보일 갯수를 넣음
    page_number = request.GET.get('page')  # url을 통해 현재 페이지가 몇 페이지인지 확인하기 위함
    page_obj = paginator.get_page(page_number)  # 위에서 생성한 객체에 페이지 번호를 줘서 해당 페이지에 출력되어야 할 데이터를 가져와서 저장

    context = {
        'obj_list': page_obj.object_list,  # 가져온 페이지 데이터를 리스트형태로 형변환 해서 저장
        'page_obj': page_obj,
        'search': search,
    }



    return render(request, 'reflected_board/index.html', context)


def create(request):
    alert_message = ''

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        password = request.POST.get('password')

        if not title:
            alert_message = '제목을 입력하세요'
        elif not body:
            alert_message = '내용을 입력하세요'
        elif not password:
            alert_message = '비밀번호를 입력하세요'
        else:
            today = date.today()

            new_board = board.objects.create(title=title, body=body, password=password, created_at=today)

            alert_message = '설공적으로 글을 생성하였습니다.'
            return redirect('board_detail', board_id=new_board.id)

    context = {
        'alert_message': alert_message,
    }

    return render(request, 'board/create.html', context)


def detail(request, board_id):
    post = get_object_or_404(board, pk=board_id)

    if request.method == 'POST':
        password = request.POST.get('password')
        delORupt = request.POST.get('action')

        if password == post.password:
            print(delORupt)
            if delORupt == 'delete':
                post.delete()
                return redirect('reflected_board:board_index')
            elif delORupt == 'update':
                return redirect('reflected_board:board_update', board_id=board_id)
            # else:
            # 404페이지 리턴

        # else:
        # 잘못된 비밀번호 입니다 alert

    context = {
        'title': post.title,
        'body': post.body,
        'id': post.id,
    }

    return render(request, 'reflected_board/detail.html', context)


def update(request, board_id):
    post = get_object_or_404(board, pk=board_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        password = request.POST.get('password')
        post.title = title
        post.body = body
        post.password = password
        post.save()
        return redirect('board_index')

    context = {
        'id': post.id,
        'title': post.title,
        'body': post.body,
    }

    return render(request, 'board/update.html', context)
