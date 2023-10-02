from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from .serializers import (
    MenuItemSerializer,
    UserSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer
)
from .models import MenuItem, Cart, Order, OrderItem
from datetime import datetime

# Create your views here.

ROLES = ['Manager', 'Delivery Crew', 'Customer']




# class MenuItemsListView(generics.ListAPIView):
#     queryset = MenuItem.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = MenuItemSerializer
    
#     def get(self, request, *args, **kwargs):
#         user_role = check_user_role(request.user, ROLES)
#         if user_role == ROLES[1] or user_role == 'Customer':
#             menu_items = MenuItem.objects.all()
#             serialized_data = MenuItemSerializer(menu_items, many=True)
#             return Response(serialized_data.data, status.HTTP_200_OK)
#         return Response({'message': 'you cant access menu items'})


# class MenuItemsViewSet(viewsets.ModelViewSet):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

#     @action(detail=False, methods=['get'])
#     def menu_items(self, request):
#         user_role = check_user_role(request.user, ROLES)
#         if user_role == ROLES[1] or user_role == 'Customer':
#             menu_items = self.get_queryset()
#             serialized_data = self.serializer_class(menu_items, many=True)
#             return Response(serialized_data.data, status=status.HTTP_200_OK)
#         return Response({'message': 'You can\'t access menu items'}, status=status.HTTP_403_FORBIDDEN)

#     @action(detail=False, methods=['post', 'put', 'patch', 'delete'])
#     def deny_access(self, request):
#         return Response({'message': 'Denies access'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def menu_items_view(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        serialized_data = MenuItemSerializer(menu_items, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        is_admin = request.user.is_superuser
        is_manager = check_user_role(request.user, ROLES) == ROLES[0]
        if not is_admin and not is_manager:
            return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)
        serialized_data = MenuItemSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'message': 'Success', 'data': serialized_data.data}, status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid Data', 'Errors': serialized_data.errors}, status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def menu_item_detailed_view(request, id, *args, **kwargs):
    if request.method == 'GET':
        if not id:
            return Response({'message': 'Invalid id'}, status.HTTP_400_BAD_REQUEST)
        try:
            menu_item = MenuItem.objects.get(id=id)
            serialized_data = MenuItemSerializer(menu_item)
            return Response(serialized_data.data, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid id'}, status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT' or request.method == 'PATCH':
        is_admin = request.user.is_superuser
        is_manager = check_user_role(request.user, ROLES) == ROLES[0]
        if not is_admin and not is_manager:
            return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)
        try:
            menu_item = MenuItem.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid id'}, status.HTTP_400_BAD_REQUEST)
        
        serialized_data = MenuItemSerializer(menu_item, data=request.data, partial=request.method == 'PATCH')
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'message': 'Success', 'data': serialized_data.data}, status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid Data', 'Errors': serialized_data.errors}, status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        is_admin = request.user.is_superuser
        is_manager = check_user_role(request.user, ROLES) == ROLES[0]
        if not is_admin and not is_manager:
            return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)
        try:
            menu_item = MenuItem.objects.get(id=id)
            menu_item.delete()
            return Response({'message': 'Item Deleted'}, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid id'}, status.HTTP_400_BAD_REQUEST)


class ListAddManagers(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def get_queryset(self):
        is_admin = self.request.user.is_superuser
        is_manager = check_user_role(self.request.user, ROLES) == ROLES[0]
        if not is_admin and not is_manager:
            return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)
        return User.objects.filter(groups__name='Manager')
    
    def post(self, request, *args, **kwargs):
        is_admin = request.user.is_superuser
        is_manager = check_user_role(request.user, ROLES) == ROLES[0]
        if not is_admin and not is_manager:
            return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('id')
        username = request.data.get('username')
        email = request.data.get('email')
        if not any([user_id, username, email]):
            return Response({'message': 'Invalid Data'}, status.HTTP_400_BAD_REQUEST)
        try:
            if user_id:
                user = User.objects.get(id=user_id)
            elif username:
                user = User.objects.get(username=username)
            elif email:
                user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid Id'}, status.HTTP_404_NOT_FOUND)
        manager_group = Group.objects.get(name=ROLES[0])
        user_is_admin = user.is_superuser
        if user_is_admin:
            return Response({'message': 'Unaothorized'}, status.HTTP_400_BAD_REQUEST)            
        if check_user_role(user, ROLES) != ROLES[0]:
            user.groups.add(manager_group)
            return Response({'message': 'Success'}, status.HTTP_201_CREATED)
        return Response({'message': 'User Already a Manager'}, status.HTTP_200_OK)
        
class DestroyFromManager(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def delete(self, request, *args, **kwargs):
        is_admin = request.user.is_superuser
        is_manager = check_user_role(request.user, ROLES) == ROLES[0]
        if not is_admin and not is_manager:
            return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)
        user_id = self.kwargs.get('pk')
        if not user_id:
            return Response({'message': 'Invalid ID'})    
        try:
            user =User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid user'}, status.HTTP_404_NOT_FOUND)  
          
        manager_group = Group.objects.get(name=ROLES[0])
        user_is_admin = user.is_superuser
        user_is_manager = check_user_role(user, ROLES) == ROLES[0]
        if user_is_admin:
            return Response({'message': 'Unaothorized'}, status.HTTP_400_BAD_REQUEST)            
        if user_is_manager:
            user.groups.remove(manager_group)
            return Response({'message': 'Success'}, status.HTTP_201_CREATED)
        return Response({'message': 'User Not a Manager'}, status.HTTP_404_NOT_FOUND)




class ListCreateDeliveryCrew(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def get_queryset(self):
        is_admin = self.request.user.is_superuser
        is_manager = check_user_role(self.request.user, ROLES) == ROLES[0]
        if not is_admin and not is_manager:
            return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)
        return User.objects.filter(groups__name='Delivery Crew')
    
    def post(self, request, *args, **kwargs):
        is_admin = request.user.is_superuser
        is_manager = check_user_role(request.user, ROLES) == ROLES[0]
        if not is_admin and not is_manager:
            return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('id')
        username = request.data.get('username')
        email = request.data.get('email')
        if not any([user_id, username, email]):
            return Response({'message': 'Invalid Data'}, status.HTTP_400_BAD_REQUEST)
        try:
            if user_id:
                user = User.objects.get(id=user_id)
            elif username:
                user = User.objects.get(username=username)
            elif email:
                user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid Id'}, status.HTTP_404_NOT_FOUND)
        
        delivery_group = Group.objects.get(name=ROLES[1])
        user_not_delivery = check_user_role(user, ROLES) != ROLES[1]
        if user_not_delivery:
            user.groups.add(delivery_group)
            return Response({'message': 'Success'}, status.HTTP_201_CREATED)
        return Response({'message': 'User Already a Delivery'}, status.HTTP_200_OK)

class DestroyFromDelivery(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def delete(self, request, *args, **kwargs):
        is_admin = request.user.is_superuser
        is_manager = check_user_role(request.user, ROLES) == ROLES[0]
        if not is_admin and not is_manager:
            return Response({'message': 'Unauthorized'}, status.HTTP_403_FORBIDDEN)
        user_id = self.kwargs.get('pk')
        if not user_id:
            return Response({'message': 'Invalid ID'})    
        try:
            user =User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return Response({'message': 'Invalid user'}, status.HTTP_404_NOT_FOUND)  
          
        delivery_group = Group.objects.get(name=ROLES[1])
        user_is_admin = user.is_superuser
        user_is_delivery = check_user_role(user, ROLES) == ROLES[1]
        if user_is_admin:
            return Response({'message': 'Unaothorized'}, status.HTTP_403_FORBIDDEN)            
        if user_is_delivery:
            user.groups.remove(delivery_group)
            return Response({'message': 'Success'}, status.HTTP_201_CREATED)
        return Response({'message': 'User Not a Delivery'}, status.HTTP_404_NOT_FOUND)

class ListCartItems(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CartItemSerializer

    def get_queryset(self): 
        return Cart.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        user = request.user
        menu_item_id = request.data.get('id')
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        cart_obj_menu_item = Cart.objects.filter(user=user, menuitem=menu_item).first()
        if not cart_obj_menu_item:
            cart_obj_menu_item = Cart.objects.create(
                user = user,
                menuitem = menu_item,
                unit_price = menu_item.price,
                price = menu_item.price,
                quantity = 1)
            cart_obj_menu_item.save()
            return Response({'message': 'Item Created'}, status.HTTP_201_CREATED)
        quantity = cart_obj_menu_item.quantity + 1
        serialized_item = CartItemSerializer(cart_obj_menu_item, data={'quantity': quantity}, partial=True)
        if serialized_item.is_valid(raise_exception=True):
            serialized_item.save()
        return Response({'message': 'quantity updated'}, status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = request.user
        menu_item_id = request.data.get('id')
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        cart_obj_menu_item = Cart.objects.filter(user=user, menuitem=menu_item).first()
        if not cart_obj_menu_item:
            return Response({'message': 'Invalid item'}, status.HTTP_404_NOT_FOUND)
        cart_obj_menu_item.delete()
        return Response({'message': 'Item Deleted'}, status.HTTP_200_OK)
                   
        
class OrderListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer

    def get_queryset(self):
        is_admin = self.request.user.is_superuser
        is_manager = check_user_role(self.request.user, ROLES) == ROLES[0]
        is_delivery_crew = check_user_role(self.request.user, ROLES) == ROLES[1]
        if not is_admin and not is_manager and not is_delivery_crew:
            return Order.objects.filter(user=self.request.user)
        if is_delivery_crew:
            return Order.objects.filter(delivery_crew=self.request.user)
        return Order.objects.all()
    
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        if cart_items:
            order_qs = Order.objects.create(
                user=user,
                date=datetime.now(),
                total = 0
                    )
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order= order_qs,
                    menuitem=cart_item.menuitem,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price,
                    price=cart_item.price
                )
            cart_items.delete()
            return Response({'message': 'Order created successfully'}, status.HTTP_201_CREATED)
        return Response({'message': 'No cart items to create an order from'}, status.HTTP_400_BAD_REQUEST)


class orderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        is_admin = self.request.user.is_superuser
        is_manager = check_user_role(self.request.user, ROLES) == ROLES[0]
        is_delivery_crew = check_user_role(self.request.user, ROLES) == ROLES[1]
        order = Order.objects.filter(id=pk)
        if is_admin or is_manager:
            return Order.objects.filter(id=pk)
        if is_delivery_crew and order.filter(user=self.request.user):
            return Order.objects.filter(id=pk)
        return Order.objects.filter(id=pk, user=self.request.user)
    
    def update(self, request, *args, **kwargs):
            order = self.get_object()
            is_manager = check_user_role(request.user, ROLES) == ROLES[0]
            is_delivery_crew = check_user_role(request.user, ROLES) == ROLES[1]
            data = {}
            status = request.data.get('status')
            order_item_id = request.data.get('order_item')
            dc_id =  request.data.get('delivery_crew') 
            if dc_id and is_manager:
                user = User.objects.filter(id=dc_id).first()
                if not check_user_role(user, ROLES) == ROLES[1]:
                    return Response({'message': 'not a delivery crew'}, status=400)
                data['delivery_crew'] = user.id

            if status and (is_manager or is_delivery_crew):
                status = request.data.get('status')
                data['status'] = status

            if order_item_id:
                order_item = OrderItem.objects.filter(id=order_item_id, order=order).first()
                quantity_update = request.data.get('action')

                if order_item:
                    if quantity_update == 'add':
                        order_item.quantity += 1
                        order_item.save()
                        return Response({'message': 'quantity added'}, status=200)
                    elif quantity_update == 'remove':
                        if order_item.quantity > 1:
                            order_item.quantity -= 1
                            order_item.save()
                            return Response({'message': 'quantity removed'}, status=200)
                        else:
                            order_item.delete()
                            return Response({'message': 'order item deleted'}, status=200)
                    order_item.save()
                else:
                    return Response({'message': 'Invalid order item id'}, status=400)
            if data:
                serialized_data = self.get_serializer(order, data=data, partial=True)
                if serialized_data.is_valid(raise_exception=True):
                    serialized_data.save()
                    return Response({'message': 'Order updated successfully'}, status=200)
            return Response({'message': 'Noth to update'}, status=200)
    
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response({'message': 'Order deleted successfully'}, status.HTTP_200_OK)
    


# helper function
def check_user_role(user, roles):
    if isinstance(roles, list):
        for role in roles:
            if user.groups.filter(name=role).exists():
                return role
        if user.is_superuser:
            return 'Superuser'
        return 'Customer'