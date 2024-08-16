from django.contrib import admin

from main_app.models import User, Country, Type, SubType, Dish, CookingStage, Category,\
                    UnitOfMeasure, Conversion, DishCategory, \
                    Order, Menu, Shop, Product

admin.site.register(User)
admin.site.register(Country)
admin.site.register(Type)
admin.site.register(SubType)
admin.site.register(Dish)
admin.site.register(CookingStage)
admin.site.register(Category)
admin.site.register(UnitOfMeasure)
admin.site.register(Conversion)
admin.site.register(DishCategory)
admin.site.register(Order)
admin.site.register(Menu)
admin.site.register(Shop)
admin.site.register(Product)
