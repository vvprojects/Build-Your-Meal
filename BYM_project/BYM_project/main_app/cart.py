from main_app.models import Dish, Menu, Category, DishCategory, Order, UnitOfMeasure, Conversion
from main_app.search import SearchProduct
from django.utils import timezone


class Cart:
    '''! Класс для работы с карзиной пользователья
    '''
    def __init__(self, user_id):
        '''! Находит текущий Order по user_id
        @param user_id
        '''
        self.user_id = user_id
        try:
            self.order_obj = Order.objects.get(user_id=user_id, current=True)
        except Order.DoesNotExist:
            self.order_obj = Order.objects.create(user_id=user_id, order_date=timezone.now())

    def change_order(self, dish_id, add_flg):
        '''! Изменяем корзину блюд пользователя - или добавить (+1), или убрать (-1)
        @param dish_id int
        @param add_flg bool - True прибавление, False вычитание
        '''
        dish_obj = Dish.objects.get(pk=dish_id)
        menu_obj, created = Menu.objects.get_or_create(order=self.order_obj, dish=dish_obj)
        if not created:
            if add_flg:
                amount = menu_obj.amount + 1
            else:
                amount = menu_obj.amount - 1
            if amount <= 0:
                Menu.objects.filter(order=self.order_obj, dish=dish_obj).delete()
            else:
                Menu.objects.filter(order=self.order_obj, dish=dish_obj).update(amount=amount)

    def create_new_order(self, cart):
        '''! Создаём новую корзину блюд пользователя на основе cart
        @param cart [{"dish_pk": int, "amount": int}, ...]
        '''
        Order.objects.filter(user_id=self.user_id, current=True).update(current=False)
        self.order_obj = Order.objects.create(user_id=self.user_id, order_date=timezone.now())

        for x in cart:
            Menu.objects.create(order=self.order_obj, dish_id=x['dish_pk'], amount=x['amount'])

    def get_order_array(self):
        '''! Возвращает текущую корзину блюд пользователя
        @return order_array [{"dish": Dish, "amount": int}, ...]
        '''

        return Menu.objects.filter(order=self.order_obj)

    @staticmethod
    def get_categories(order_array):
        '''! Раскладывает карзину пользователя (в виде блюд), на товары если в рецептах товары в разных единицах измерения приводит к единой
        @param order_array [Menu.object, ...]
        @return categories [{"category": Category, "amount": float, "unit_name": string}, ...]
        '''
        category_dict = dict()

        for x in order_array:
            dish_category_list = DishCategory.objects.filter(dish=x.dish)

            for dish_category_obj in dish_category_list:
                category_id = dish_category_obj.category.id
                number = float(dish_category_obj.amount) * x.amount
                unit_name = dish_category_obj.unit.supreme_unit.name

                if dish_category_obj.unit.supreme_unit.name == 'по вкусу':
                    continue

                if category_id in category_dict.keys():
                    if category_dict[category_id]['unit_name'] != unit_name:
                        if category_dict[category_id]['unit_name'] == ['г', 'мл']:
                            category_dict[category_id]['amount'] += number * float(Conversion.objects.get(category=dish_category_obj.category, from_unit=dish_category_obj.unit.supreme_unit).to_unit.coefficient)
                            continue
                        prev_unit = UnitOfMeasure.objects.get(name=category_dict[category_id]['unit_name'])
                        if dish_category_obj.unit.supreme_unit.name == 'г':
                            category_dict[category_id]['unit_name'] = 'г'
                        elif dish_category_obj.unit.supreme_unit.name == 'мл':
                            category_dict[category_id]['unit_name'] = 'мл'
                        else:
                            print(dish_category_obj.category.name, dish_category_obj.unit.supreme_unit.name)
                            category_dict[category_id]['unit_name'] = Conversion.objects.get(category=dish_category_obj.category, from_unit=dish_category_obj.unit.supreme_unit).to_unit.supreme_unit.name

                        if prev_unit.name in ['г', 'мл']:
                            category_dict[category_id]['amount'] = category_dict[category_id]['amount']
                        else:
                            category_dict[category_id]['amount'] = category_dict[category_id]['amount'] * float(Conversion.objects.get(category=dish_category_obj.category, from_unit=prev_unit).coefficient)

                        if dish_category_obj.unit.name in ['г', 'мл']:
                            category_dict[category_id]['amount'] += number
                        else:
                            category_dict[category_id]['amount'] += number * float(Conversion.objects.get(category=dish_category_obj.category, from_unit=dish_category_obj.unit.supreme_unit).coefficient)
                    else:
                        category_dict[category_id]['amount'] += number
                else:
                    category_dict[category_id] = {"amount": number, "unit_name": unit_name}

        categories = []
        for key in category_dict.keys():
            category = Category.objects.get(id=key)
            amount = category_dict[key]['amount']
            amount = f'{float(amount):g}'
            unit_name = category_dict[key]['unit_name']
            if amount == 0:
                amount = None
            categories.append({"category": category, "amount": amount, "unit_name": unit_name})

        return categories

    def get_categories_list(self, slice, city, street, number):
        '''! Выдает slice наиболие подходящих товаров в каждой категории
        @param slice int
        @param city string
        @param street string
        @param number string
        @return categories_list[{"category": string, "category_amount": int, "category_unit_name": string, "product_list": [Product, ...]}, ...]
        '''
        order_array = self.get_order_array()
        categories = Cart.get_categories(order_array)

        categories_list = []
        for cat in categories:
            product_list = SearchProduct(cat["category"].id, city, street, number, 0).get()[:slice]
            for product in product_list:
                product.amount = f'{float(product.amount):g}'

            if cat["amount"] is not None:
                categories_list.append({"category": cat["category"], "category_amount": cat["amount"],
                                        "category_unit_name": cat["unit_name"], "product_list": product_list})

        return categories_list
