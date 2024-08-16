import re
import unicodedata
from main_app.models import User, Type, SubType, Dish, CookingStage, Order, DishCategory


def get_dish_types():
    '''! Запрос в бд на получение типов блюд и соответстующих им под типов
    @return dict {type:[subtype,...]}
    '''
    dic = {}
    types = Type.objects.all()
    for type in types:
        dic[type] = [subtype for subtype in SubType.objects.filter(type=type)]
    return dic


def get_particular_dish(dish_id):
    '''! Возвращает конкретное блюдо, стадии его приготовления и необходимые игридиенты
    @param dish_id int
    @return dish Dish
    @return cooking_stages [CookingStage,...]
    @return ingredients [{'name':string, amount:int}] - список ингридиентов - название категории их кол-во
    '''
    dish = Dish.objects.get(pk=dish_id)
    cooking_stages = CookingStage.objects.filter(dish=dish)
    ingredients = []
    for x in DishCategory.objects.filter(dish=dish):
        if x.amount != 0:
            amount = ' '.join([f'{float(x.amount):g}', x.unit.name])
        else:
            amount = x.unit.name
        ingredients.append({'name': x.category.name, 'amount': amount})

    return dish, cooking_stages, ingredients


def string_to_minutes(string):
    '''! Возвращает количество минут в строке
    Варианты входа: 'n часов', 'n минут', 'n часов k минут'
    @param string string
    @return int
    '''
    nums = [int(x) for x in re.findall(r'\d+', string)]
    if 'час' in string:
        if 'мин' in string:
            return nums[0] * 60 + nums[1]
        else:
            return nums[0] * 60
    else:
        return nums[0]


def convert_fraction(string):
    '''! Возвращает float из строки с числом
    @param string string
    @return float
    '''
    string = string.replace(',', '.')
    if len(string) == 1:
        return unicodedata.numeric(string)
    return float(string)


def number_and_measure(string):
    '''! Возвращает по строке количества продукта число + единицу измерения в начальной форме
    @param string string
    @return float
    @return string
    '''
    words = string.split()
    if len(words) >= 2 and (words[0].isnumeric() or '.' in words[0] or ',' in words[0]):
        return convert_fraction(words[0]), ' '.join(words[1:])
    else:
        return 0.0, ' '.join(words)
