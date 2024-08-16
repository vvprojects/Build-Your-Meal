from main_app.models import Dish, Category, Product
from difflib import SequenceMatcher
from django.db.models import Q
from main_app.recommendation_system import RecommendationSystem


class SearchDish:
    '''!
    Класс реализует функционал поиска и сортировки блюд по строке поиска, фильтрам блюда,
    рекомендациям конткретному пользователю и указанному адресу
    '''

    def __init__(self, types=None, subtypes=None, search_string='', address_flg=0, user_id=None, ratio=1,
                 threshold=0) -> None:
        '''!    
        Инициализирует класс списком блюд, делая запрос в базу данных
        @param types=[] list of int
        @param subtypes=[] list of int
        @param search_string='' str
        @param adress_flg=0 int
        @param user_id=None int
        @param ratio float (во сколько раз рекомендательная система важнее совпадения строк)
        '''

        self.threshold = threshold
        if subtypes is None:
            subtypes = []
        if types is None:
            types = []
        self.search_string = search_string
        self.address_flg = address_flg

        if ratio < 0:
            raise ValueError("Ratio is less than 0")
        else:
            self.ratio = ratio

        if subtypes.__len__():
            if types.__len__():
                self.dish_list = Dish.objects.filter(Q(subtype__id__in=subtypes) | Q(subtype__type__id__in=types))
            else:
                self.dish_list = Dish.objects.filter(subtype__id__in=subtypes)
        else:
            if types.__len__():
                self.dish_list = Dish.objects.filter(subtype__type__id__in=types)
            else:
                self.dish_list = Dish.objects.all()

    def score(self, dish) -> float:
        '''!
        Сопосталяет каждому объекту класса Dish число, по которому будет осуществлена сортировка
        @param dish Dish
        @return score double
        '''
        sm_score = self.seq_match_scorer(dish)
        rec_score = self.recommend_scorer(dish)
        score = sm_score / (self.ratio + 1) + rec_score * self.ratio / (self.ratio + 1)
        if type(self.search_string) is str:
            strings = self.search_string.lower().split()
            for s in strings:
                if s in dish.name.lower():
                    score += 1
        return score

    def get(self, slice) -> list:
        '''!
        Сортирует список объектов класса Dish
        @return dish_list list of Dish
        '''
        new = sorted(self.dish_list, key=self.score, reverse=True)
        for i in range(len(new)):
            if self.score(new[i]) < self.threshold:
                return new[:min(i, slice)]
        return new[:slice]

    def recommend_scorer(self, dish) -> float:
        '''! Предсказывает вес нравящности для блюда и пользователя.
        @param dish Dish
        @return weight double
        '''

        return 0

    def seq_match_scorer(self, dish) -> float:
        '''!
        Сравнивает Dish.name и self.search_string с помощью SequenceMather()
        @param dish Dish
        @return sm_score float
        '''
        if dish is None:
            return 0
        if not dish.name or dish.name is None:
            return 0
        if not self.search_string:
            return 0
        s = SequenceMatcher(a=self.search_string, b=dish.name)
        sm_score = s.ratio()
        return sm_score


class SearchProduct:
    '''!
    1. Загружаем из бд список всех спаршенных продуктов
    2. Вызов функции SequenceMatch() (взвешиваем каждый product.name относительно category.name по похожести)
    3. Сортируем продукты по убыванию весов и эффективности покупки
    @param category_id int
    @return products [[Product obj, ...], [Category.name, [image1, ...]]]]
    '''

    def __init__(self, category_id, city, street, number, threshold=0.9) -> None:
        '''!
        @param category_id int
        '''

        self.category = Category.objects.get(id=category_id)
        self.products = Product.objects.filter(address_city=city, address_street=street, address_number=number)
        self.threshold = threshold

    def score(self, product) -> float:
        '''!
        Сопосталяет каждому объекту класса Product число, по которому будет осуществлена сортировка
        @param product Product
        @return score double
        '''

        sm_score = self.seq_match_scorer(product)
        if type(self.category.name) is str:
            strings = self.category.name.lower().split()
            for s in strings:
                if s in product.name.lower():
                    sm_score += 1
        return sm_score

    def get(self) -> list:
        '''!
        Сортирует список объектов класса Product
        @return products list of Product
        '''
        new = sorted(self.products, key=self.score, reverse=True)
        for i in range(len(new)):
            if self.score(new[i]) < self.threshold:
                return new[:i]
        return new

    def seq_match_scorer(self, product) -> float:
        '''!
        Сравнивает Product.name и self.category.name с помощью SequenceMather()
        @param product Product
        @return sm_score float
        '''
        if product is None:
            return 0
        if not product.name or product.name is None:
            return 0
        if not self.category.name or self.category.name is None:
            return 0
        s = SequenceMatcher(a=self.category.name, b=product.name)
        sm_score = s.ratio()
        return sm_score

    def get_category(self) -> Category:
        '''!
        Возвращает self.category
        @return category Category
        '''
        return self.category
