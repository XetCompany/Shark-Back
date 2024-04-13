from django.contrib import admin

from app.models import *

all_models = [ProductCategory, ProductCompany, City, PointInCity, ProductInWarehouse, Path, GroupPath, GroupPathsRelation, GroupPaths, SearchInfo, OrderProduct, Order, CartProduct, Cart, User, ResetPasswordToken, EvaluationAndComment, Notification]

# Register your models here.
for model in all_models:
    admin.site.register(model)
