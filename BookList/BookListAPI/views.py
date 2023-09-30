from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from .serializers import BookSerializer, CategorySerializer, MenuItemSerializer
from rest_framework.decorators import api_view

from .models import Book, MenuItem, Category

# Create your views here.

@csrf_exempt
def books(request):
    if request.method == 'GET':
        books = Book.objects.all()
        book_list = [model_to_dict(book) for book in books]
        return JsonResponse({'books': book_list})
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        inventory = request.POST.get('inventory')

        book = Book.objects.create(title=title, author=author, price=price, inventory=inventory)
        try:
            book.save()
        except IntegrityError:
            return JsonResponse({'error': 'true', 'message': 'required field missing', status: 400})
            
        return JsonResponse(model_to_dict(book))
    
    
    return JsonResponse({'error': 'Invalid http method'})

def display_even_numbers(request):
    response = ""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in numbers:
        remainder = i % 2
        if remainder == 0:
            response += str(i) + "<br/>"
    return HttpResponse(response)


class Books(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


########### apply filtering and ordering for class based views
class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields=['price', 'inventory']
    search_fields=['title']
    # search_fields=['title', 'category_title']

####### function based views#####################
@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data) 

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serializer_data = MenuItemSerializer(items, many=True, context = {'request': request})
        return Response(serializer_data.data)

    if request.method == 'POST':
        serializer_data = MenuItemSerializer(data=request.data, context = {'request': request})
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
        return Response(serializer_data.data, status.HTTP_201_CREATED)
    
@api_view()
def single_item(request, id):
    item = MenuItem.objects.get(pk=id)
    serialized_item = MenuItemSerializer(item, context = {'request': request})
    return Response(serialized_item.data, status.HTTP_200_OK)