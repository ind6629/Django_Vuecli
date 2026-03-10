from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from ..models import Product, TrackSearch
import json

def load(request):
    curr_user_id = request.GET.get('user_id')
    keyword = request.GET.get('keyword', '')
    
    # Search products with case-insensitive name matching
    products = Product.objects.filter(name__icontains=keyword)
    
    # Prepare data for Kafka
    dict_data = [{
        'product_id': item.id,
        'category': item.category,
    } for item in products]
    
    # Kafka producer setup would go here
    # producer = KafkaProducer(...)
    
    # Create track search records and send to Kafka
    for item in dict_data:
        TrackSearch.objects.create(
            product_id=item['product_id'],
            user_id=curr_user_id,
            category=item['category']
        )
        # Kafka send would go here
        # producer.send('search', {
        #     'user_id': curr_user_id,
        #     'product_id': item['product_id'],
        #     'category': item['category']
        # })
    
    if not keyword:
        keyword = "any"
    
    return render(request, 'searchResult.html', {
        'products': products,
        'keyword': keyword
    })