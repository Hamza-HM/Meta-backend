from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User
from rest_framework.validators import  UniqueTogetherValidator, UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'title',
            'featured',
            'price',
            'category',
            'category_id'
        ]
        extra_kwargs = {
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItem.objects.all()
                    )
                ]
            }
        }
        # depth = 1


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields= [
            'id',
            'menuitem',
            'quantity',
            'unit_price',
            'price',
                  ]
    def get_price(self, obj):
        return obj.unit_price * obj.quantity
    
class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields= [
            'id',
            'menuitem',
            'quantity',
            'unit_price',
            'price',
                  ]
    def get_price(self, obj):
        return obj.unit_price * obj.quantity
        
class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    orderitems = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields= [
            'id',
            'user',
            'delivery_crew',
            'status',
            'total',
            'date',
            'orderitems'
                  ]
        
    def get_orderitems(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serialized_order_items = OrderItemSerializer(order_items, many=True)
        if serialized_order_items:
            return serialized_order_items.data
        else:
            return serialized_order_items.errors

        
    def get_total(self, obj):
        total = 0
        for order_item in obj.orderitem_set.all():
            total += order_item.price
        return total