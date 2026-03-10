from django.urls import path
from ..views.main import index
from ..views.main import help
from ..views.main import about
from ..views.main import product_detail
from ..views.main import category
from ..views.main import add_product
from ..views.main import edit_product
from ..views.main import checkout
from ..views.main import addOrder
from ..views.main import collect
from ..views.main import products
from ..views.main import news
from ..views.main import search

urlpatterns = [
    path('', index, name="main_index"),
    path('help', help, name="main_help"),
    path('about', about, name="main_about"),
    path('api/productDetail/<int:productId>', product_detail, name="main_product_detail"),
    path('category', category, name="main_category"),
    path('add_product', add_product, name="main_add_product"),
    path('edit_product/<int:product_id>', edit_product, name="main_edit_product"),
    path('checkout', checkout, name="main_checkout"),
    path('addOrder', addOrder, name="main_addOrder"),
    path('collect/<int:user_id>/<int:product_id>/<str:is_collected>/', collect, name="main_collect"),
    path('api/products/<str:productType>', products, name="main_products"),
    path('api/news', news, name="main_news"),
    path('api/search', search, name="search"),
]