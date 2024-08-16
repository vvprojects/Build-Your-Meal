from main_app.search import SearchDish
from main_app.functions_backend import get_particular_dish
from main_app.cart import Cart
from main_app.models import User, Product, UnitOfMeasure
from main_app.parser import parse_by_address
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
import json
from django.utils import timezone
from main_app.conversions_functions import how_many_add


# возвращает на frontend json с блюдами по поисковой строке
class SearchDishApi(APIView):
    def post(self, request):
        search_string = request.data['searchString']
        if search_string == '':
            search_string = None
        
        search_dish = SearchDish(search_string=search_string)
        object_list = search_dish.get(slice=12)

        return Response({'object_list': json.loads(serializers.serialize('json', object_list))})


# изменяет корзину блюд пользователя в БД
class ChangeCartApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        cart_change = request.data['cartChange']

        user_id = request.user.id
        cart_obj = Cart(user_id)

        cart_obj.change_order(cart_change['dish_pk'], cart_change['add_flg'])
        order_array = cart_obj.get_order_array()

        cart = []
        for x in order_array:
            cart.append({'dish_pk': x.dish.pk, 'name': x.dish.name, 'amount': x.amount})

        return Response(cart)


# синхронизирует корзину блюд пользователя в БД и на фронте
class SyncCartApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        cart = request.data['cart']

        user_id = request.user.id
        cart_obj = Cart(user_id)

        if len(cart) == 0:
            order_array = cart_obj.get_order_array()
            cart = []
            for x in order_array:
                cart.append({'dish_pk': x.dish.pk, 'name': x.dish.name, 'amount': x.amount})
        else:
            cart_obj.create_new_order(cart)
        return Response(cart)


# запускает парсер продуктов Лавки по переданному адресу
class ParseProductsApi(APIView):
    def post(self, request):
        address = request.data['address']
        city = address['city']
        street = address['street']
        number = address['number']

        now_time = timezone.now()
        Product.objects.filter(created__lt=(now_time - timezone.timedelta(days=1))).delete()

        if len(Product.objects.filter(address_city=city, address_street=street, address_number=number)) == 0:
            parse_by_address(city, street, number)
            return Response(1)

        return Response(0)


# возвращает на frontend словарь с информацией о блюде
class LoadDishDataApi(APIView):
    def post(self, request):
        dish_pk = request.data['dish_pk']
        dish, cooking_stages, ingredients = get_particular_dish(dish_pk)

        recipe = []
        for x in cooking_stages:
            recipe.append({'order': x.order, 'description': x.description})

        return Response({'dish_name': dish.name, 'dish_image': str(dish.image), 'ingredients': ingredients,
                         'calories': dish.calories, 'proteins': dish.proteins, 'fats': dish.fats, 'carbohydrates': dish.carbohydrates,
                         'recipe': recipe})


# возвращает на frontend json с блюдами по поисковой строке
class RegisterApi(APIView):
    def post(self, request):
        data = request.data['user_data']

        username = data['username']
        password = data['password']

        User.objects.create_user(username=username, password=password)

        return Response(1)


# (сделано с костылём) возвращает на frontend словарь с категориями и подходящими для них продуктами
class LoadProductsApi(APIView):
    def post(self, request):
        address = request.data['address']
        city = address['city']
        street = address['street']
        number = address['number']

        unique_addresses = Product.objects.values('address_city', 'address_street', 'address_number').distinct()
        for x in unique_addresses:
            try:
                latest_time_record = Product.objects.filter(address_city=x['address_city'],
                                                            address_street=x['address_street'],
                                                            address_number=x['address_number']).latest('created')
                Product.objects.filter(address_city=x['address_city'],
                                       address_street=x['address_street'],
                                       address_number=x['address_number']
                                       ).exclude(created=latest_time_record.created).delete()
            except Product.DoesNotExist:
                pass

        tmp_user = None
        if request.user.id is None:
            now = timezone.now()
            tmp_user = User.objects.create_user(username=str(now), password=str(now))
            user_id = tmp_user.pk
            cart_obj = Cart(user_id)
            cart_obj.create_new_order(request.data['cart'])
        else:
            user_id = request.user.id
            cart_obj = Cart(user_id)

        categories_list = cart_obj.get_categories_list(4, city, street, number)

        final = []
        for x in categories_list:
            product_list = []
            for y in x['product_list']:
                quantity = how_many_add(x["category"],
                                        UnitOfMeasure.objects.get(name=x['category_unit_name']),
                                        y.unit,
                                        float(x["category_amount"]),
                                        float(y.amount))
                product_list.append({'name': y.name, 'link': y.link,
                                     'amount': y.amount, 'price': y.price,
                                     'product_unit_name': y.unit.name, 'quantity': quantity})

            final.append({"category": x["category"].name, "category_amount": x["category_amount"],
                          "category_unit_name": x["category_unit_name"],
                          "product_list": product_list})

        if tmp_user is not None:
            User.objects.filter(id=user_id).delete()

        return Response(final)


# передаём на фронт последний адрес пользователя из БД
class LoadLastAddressApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = User.objects.get(id=request.user.id)

        if len(Product.objects.filter(address_city=user.last_address_city, address_street=user.last_address_street, address_number=user.last_address_number)) == 0:
            return Response(1)

        return Response({'city': user.last_address_city,
                         'street': user.last_address_street,
                         'number': user.last_address_number})


# устанавливаем на БД последний адрес пользователя из фронта
class SetLastAddressApi(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        address = request.data
        city = address['city']
        street = address['street']
        number = address['number']

        User.objects.filter(id=request.user.id).update(last_address_city=city,
                                                       last_address_street=street,
                                                       last_address_number=number)

        return Response(1)
