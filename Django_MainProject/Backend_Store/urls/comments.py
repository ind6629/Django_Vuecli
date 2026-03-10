from django.urls import path
from ..views.comments import add_comment

urlpatterns = [
    path('comment/<int:product_id>', add_comment, name="comments_add_comment"),
]