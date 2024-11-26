from django.shortcuts import render
from django.db import connection


# Create your views here.

def index(request):
    query= "SELECT * FROM board_board"

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()


    context ={
        'rows':rows,
    }

    return render(request, 'board/index.html',context)