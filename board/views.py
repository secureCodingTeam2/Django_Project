from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator

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