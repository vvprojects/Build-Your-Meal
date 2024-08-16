import math
from main_app.models import Conversion, UnitOfMeasure


def how_many_add(category_id, need_unit, have_unit, need, have):
    '''! Расчет сколько штук товара необходимо купть на что бы полностью покрыть рецепт
    @param category_id int
    @param need_unit UnitOfMeasure - еденицы измерения продукта по рецепту (например стаканы)
    @param have_unit UnitOfMeasure - еденицы измерения товара из магазина (например граммы)
    @param need int - необходимое количество по рецепту (например 5, have_unit - стаканы)
    @param have int - количество в одном юните в магазине (например 500, have_unit-граммы)
    @return kol int - сколько нужно заказать
    '''

    if need_unit == UnitOfMeasure.objects.get(pk=41) or have_unit == UnitOfMeasure.objects.get(pk=41):
        return -1

    if need_unit == UnitOfMeasure.objects.get(pk=13):
        need = need * 1000
        need_unit = UnitOfMeasure.objects.get(pk=7)
    elif need_unit == UnitOfMeasure.objects.get(pk=16):
        need = need * 1000
        need_unit = UnitOfMeasure.objects.get(pk=1)

    if have_unit == UnitOfMeasure.objects.get(pk=13):
        have = have * 1000
        need_unit = UnitOfMeasure.objects.get(pk=7)
    elif have_unit == UnitOfMeasure.objects.get(pk=16):
        have = have * 1000
        need_unit = UnitOfMeasure.objects.get(pk=1)

    if have_unit == need_unit:
        pass
    elif have_unit == UnitOfMeasure.objects.get(pk=1) or have_unit == UnitOfMeasure.objects.get(pk=7):
        coef = Conversion(category=category_id, from_unit=need_unit, to_unit=have_unit).coefficient
        need = need * coef
    elif need_unit == UnitOfMeasure.objects.get(pk=1) or need_unit == UnitOfMeasure.objects.get(pk=7):
        coef = Conversion(category=category_id, from_unit=have_unit, to_unit=need_unit).coefficient
        need = need / coef
    else:
        return 0
    kol = math.ceil(need / have)
    return kol


def get_lavka_unit_id(name_unit):
    '''! Исчет единицу измерения из магазина в базе данных, если нет создает
    @param name_unit string
    @return UnitOfMeasure
    '''
    units = UnitOfMeasure.objects.filter(name=name_unit)
    if units.exists():
        for x in units:
            return x.supreme_unit
    else:
        '''
        send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['sdgssdfsdf@mail.ru'],
            fail_silently=False,
        )
        '''
        _, created = UnitOfMeasure.objects.get_or_create(supreme_unit=UnitOfMeasure.objects.get(pk=41), name=name_unit)
        return UnitOfMeasure.objects.get(pk=41)
