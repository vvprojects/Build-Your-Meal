from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''! Информация о пользователе. <br>
    last_address – последний адрес, с которого пользователь заказывал <br>
    '''

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    last_address_city = models.CharField(max_length=50, null=True, blank=True)
    last_address_street = models.CharField(max_length=50, null=True, blank=True)
    last_address_number = models.CharField(max_length=50, null=True, blank=True)


class Country(models.Model):
    '''! Таблица с кухнями различных стран <br>
    name – название кухни (например Русская кухня) <br>
    '''

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    name = models.CharField(max_length=30)


class Type(models.Model):
    '''! таблица с типами блюд <br>
    name – название типа (например Завтраки) <br>
    '''

    class Meta:
        verbose_name = 'Тип бдюда'
        verbose_name_plural = 'Типы блюд'

    name = models.CharField(max_length=30)


class SubType(models.Model):
    '''! таблица с подтипами блюд <br>
    name – название подтипа (например фруктовые десерты) <br>
    type_id – тип к которому относится подтип <br>
    '''

    class Meta:
        verbose_name = 'Подтип блюда'
        verbose_name_plural = 'Подтипы блюд'

    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)


class Dish(models.Model):
    '''! информация о блюде <br>
    name – названия блюда <br>
    pers_num – кол-во порций <br>
    cooking_time_minutes – время готовки в минутах <br>
    calories – кол-во калорий в блюде <br>
    proteins – кол0белки в блюде <br>
    carbohydrates – углеводы в блюде <br>
    fats – жиры <br>
    country_id – страна из кухни которой это блюдо (например итальянская кухня) <br>
    subtype_id – подтип блюда (например, фруктовые десерты) <br>
    image – ссылка на изображения блюда <br>
    '''

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    subtype = models.ForeignKey(SubType, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    pers_num = models.PositiveIntegerField()
    cooking_time_minutes = models.PositiveIntegerField()
    image = models.ImageField(null=True, blank=True, max_length=130)
    calories = models.PositiveIntegerField()
    proteins = models.PositiveIntegerField()
    carbohydrates = models.PositiveIntegerField()
    fats = models.PositiveIntegerField()


class CookingStage(models.Model):
    '''! шаги для приготовления блюда <br>
    description – текст того, что нужно сделать на этом шаге <br>
    order – порядковый номер шага <br>
    dish_id – блюдо, к которому относится этот шаг <br>
    image – ссылка на изображение шага <br>
    '''

    class Meta:
        verbose_name = 'Этап приготовления блюда'
        verbose_name_plural = 'Этапы приготовления блюд'

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    description = models.TextField()
    order = models.PositiveIntegerField()
    image = models.ImageField(null=True, blank=True, max_length=130)


class Category(models.Model):
    '''! категории различных продуктов для приготовления <br>
    name – название категории (например: бакалея или помидоры) <br>
    supreme_category_id – надкатегория (например надкатегорией римских помидор являются помидоры) <br>
    '''

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'

    supreme_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=70)


class UnitOfMeasure(models.Model):
    '''! единицы изменения <br>
    name – название единицы измерения (например штуки или кг) <br>
    supreme_unit_id – основная форма категории (например Supreme_unit_id у "штуки" это "штука") <br>
    '''

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    supreme_unit = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=20)


class Conversion(models.Model):
    '''! коэффициенты для перевода единиц измерения <br>
    coefficient – число на которое нужно умножить что бы перевести from_unit_id в to_unit_id <br>
    category_id – категория для которой выполняется перевод (очевидно что коэффициент для перевода штук в граммы для помидоров и огурцов отличается) <br>
    from_unit_id– единица измерения из которой выполняется перевод <br>
    to_unit_id – единица измерения в которую выполняется перевод <br>
    '''

    class Meta:
        verbose_name = 'Преобразование единицы измерения'
        verbose_name_plural = 'Преобразования единиц измерения'

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    from_unit = models.ForeignKey(UnitOfMeasure, related_name='from_unit', on_delete=models.CASCADE)
    to_unit = models.ForeignKey(UnitOfMeasure, related_name='to_unit', null=True, blank=True, on_delete=models.CASCADE)

    coefficient = models.DecimalField(max_digits=4 + 4, decimal_places=4, default=1)


class DishCategory(models.Model):
    '''! информация о составе блюда. <br>
    amount – кол-во продукта в блюде <br>
    category_id – категория продукта <br>
    dish_id – блюдо к которому относится продукт <br>
    unit_id – единицы измерения в которых указано кол-во <br>
    '''

    class Meta:
        verbose_name = 'Продукт в блюде'
        verbose_name_plural = 'Продукты в блюдах'

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(UnitOfMeasure, null=True, blank=True, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=4 + 4, decimal_places=4)


class Order(models.Model):
    '''! информация о заказах. <br>
    order_date – дата заказа <br>
    current – статус (выполнен/ не выполнен) <br>
    user_id – пользователь совершивший заказ <br>
    '''

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    order_date = models.DateTimeField()
    current = models.BooleanField(default=True)


class Menu(models.Model):
    '''! состав заказа <br>
    amount– кол-во товара, которое было заказано <br>
    dish_id – товар который был заказан <br>
    order_id – заказ в котором этот товар был заказан <br>
    '''

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    amount = models.PositiveIntegerField(default=1)


class Shop(models.Model):
    '''! информация о магазине <br>
    name – название магазина <br>
    link – ссылка на магазин <br>
    '''

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    name = models.CharField(max_length=30)
    link = models.URLField()


class Product(models.Model):
    '''! информация о конкретном товаре в магазине <br>
    name – название товара <br>
    price – цена <br>
    amount – количество (в unit_id) товара которое в одной единице заказ (например 300, unit_id – граммы) <br>
    link – ссылка на товар <br>
    shop_id – магазин, из которого товар <br>
    unit_id – единица измерения <br>
    user_id – пользователь для которого был спаршен данный товар <br>
    '''

    class Meta:
        verbose_name = 'Продукт из магазина'
        verbose_name_plural = 'Продукты из магазинов'

    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=4 + 4, decimal_places=4)
    link = models.URLField()
    address_city = models.CharField(max_length=50)
    address_street = models.CharField(max_length=50)
    address_number = models.CharField(max_length=50)
    created = models.DateTimeField()
