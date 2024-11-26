from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.core.paginator import Paginator
from .models import board

# Create your views here.

def index(request):
    query= "SELECT * FROM board_board ORDER BY id DESC"

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    paginator = Paginator(rows, 4) #페이지네이션을 위한 객체 생성, 파라미터로는 값과 한 페이지에 보일 갯수를 넣음
    page_number = request.GET.get('page') # url을 통해 현재 페이지가 몇 페이지인지 확인하기 위함
    page_obj = paginator.get_page(page_number) #위에서 생성한 객체에 페이지 번호를 줘서 해당 페이지에 출력되어야 할 데이터를 가져와서 저장

    context ={
        'obj_list':page_obj.object_list, # 가져온 페이지 데이터를 리스트형태로 형변환 해서 저장
        'page_obj':page_obj,
    }

    return render(request, 'board/index.html',context)

def input(request):
    return render(request, 'board/input.html')

def create(request):
    title = request.POST.get('title')
    body = request.POST.get('content')
    passwd = request.POST.get('passwd')
    new_post = board(title=title, body=body, password=passwd)
    new_post.save()
    return redirect('board:detail', post_id=new_post.id)

def detail(request, post_id):
    post = get_object_or_404(board,pk=post_id)
    context = {'post': post}
    return render(request,'board/detail.html', context)

def delete(request,post_id):
    post = get_object_or_404(board, pk=post_id)
    post.delete()
    return redirect('board:board_index')

def editform(request,post_id):
    post = get_object_or_404(board, pk=post_id)
    context = {'post': post}
    return render(request, 'board/edit.html', context)

def edit(request, post_id):
    post = get_object_or_404(board, pk=post_id)

    title = request.POST.get('title', post.title)
    body = request.POST.get('body', post.body)
    passwd = request.POST.get('passwd', post.password)

    post.title = title
    post.body = body
    post.password = passwd

    # 저장
    post.save()

    return redirect('board:detail', post_id=post.id)