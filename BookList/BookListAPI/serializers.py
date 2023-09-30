import bleach
from .models import Book, MenuItem
from rest_framework import serializers

from decimal import Decimal
from .models import MenuItem, Category 

from rest_framework.validators import  UniqueValidator, UniqueTogetherValidator

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# class MenuItemsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MenuItem
#         fields = [
#             'id',
#             'title',
#             'price',
#             'inventory'
#         ]

class CategorySerializer (serializers.ModelSerializer):
     class Meta:
        model = Category
        fields = ['id','slug','title']

# class MenuItemSerializer(serializers.ModelSerializer):
#     stock = serializers.IntegerField(source='inventory')
#     price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
#     category = CategorySerializer(read_only=True)
#     # category = serializers.HyperlinkedRelatedField(
#     #     queryset = Category.objects.all(),
#     #     view_name= 'category-detail'
#     # )
#     class Meta:

#         model = MenuItem
#         fields = ['id','title','price','stock', 'price_after_tax','category']
#         # depth = 1
    
#     def calculate_tax(self, product:MenuItem):
#         return product.price * Decimal(1.1)
    
class MenuItemSerializer(serializers.ModelSerializer):
    #to remember unique validator
    # title = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=MenuItem.objects.all())])
    #
    stock = serializers.IntegerField(source="inventory")
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        # validators = [ # validating two fields that must be unique together
        #     UniqueTogetherValidator(
        #         queryset=MenuItem.objects.all(),
        #         fields=['title', 'price']
        #     )
        # ]
        # extra_kwargs = {
        #     'price': {'min_value': 2},
        #     'title': {
        #         'validators': [ #unique validator for title or any field
        #             UniqueValidator( 
        #                 queryset=MenuItem.objects.all()
        #             )
        #         ]
        #     }
        # }
    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
    
    #validating data with bleach library
    def validate_title(self, value):
        return bleach.clean(value)
    # validating data
    # def validate_stock(self, value):
    #     if (value < 0):
    #         raise serializers.ValidationError('Stock cannot be negative')
    # def validate(self, attrs):
    #     attrs['title'] = bleach.clean(attrs['title'])
    #     if(attrs['inventory'] < 0):
    #         raise serializers.ValidationError('Stock cannot be negative')
    #     if(attrs['price'] < 2):
    #         raise serializers.ValidationError('Price should not be less than 2.0')
    #     return super().validate(attrs)

    
# class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
#     stock = serializers.IntegerField(source='inventory')
#     price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
#     class Meta:

#         model = MenuItem
#         fields = ['id','title','price','stock', 'price_after_tax','category']
#         # depth = 1
    
#     def calculate_tax(self, product:MenuItem):
#         return product.price * Decimal(1.1)