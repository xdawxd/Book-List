from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from books.api.serializers import BookSerializer
from books.models import Book


@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def book_create(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
