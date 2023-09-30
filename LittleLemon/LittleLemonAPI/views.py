from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from .serializers import MenuItemSerializer
from .models import MenuItem
# Create your views here.


class MenuItemsListView(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MenuItemSerializer
    
    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user.groups.filter(name='Delivery Crew').exists():
            return Response({'message': 'this is a delivery crew'})
        return Response({'message': 'check another one'})