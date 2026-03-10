from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from datetime import datetime, timedelta
from ..models import (
    TrackClick, TrackSearch, TrackCart, TrackOrder,
    Clickresult_Sparkstream, SearchResult_Sparkstream,
    Cartresult_Sparkstream, Orderesult_Sparkstream,
    Product
)
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.db.models.functions import TruncDate, TruncDay
from django.utils import timezone 
import json

def init(request):
    return render(request, 'analysis.html')

def realtime_init(request):
    return render(request, 'realtime_analysis.html')

@csrf_exempt
def clickData(request):
    product_interaction_counts = TrackClick.objects.values(
        'product_id'
    ).annotate(
        interaction_count=Count('user_id')
    ).order_by('product_id')
    
    data = list(product_interaction_counts)
    for item in data:
        product = Product.objects.filter(id=item['product_id']).first()
        item['name'] = product.name if product else ''
        
    return JsonResponse({'data':data})

def searchData(request):
    keywords_search_counts = TrackSearch.objects.values(
        'category'
    ).annotate(
        search_count=Count('id')
    )
    
    data = list(keywords_search_counts)
    #print("data",data)
    return JsonResponse({'data':data})

def cartData(request):
    cart_category_counts = TrackCart.objects.values(
        'category'
    ).annotate(
        count=Count('id')
    )
    
    data = list(cart_category_counts)
    return JsonResponse({'data':data})

def orderData(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    result = TrackOrder.objects.filter(
        timestamp__gte=start_date,
        timestamp__lte=end_date,
        category__isnull=False
    ).extra(
        {'date': "DATE(timestamp)"}
    ).values(
        'date', 'category'
    ).annotate(
        count=Count('category')
    ).order_by('date', '-count')
    
    daily_top_categories = {}
    for row in result:
        date_str = row['date'].strftime('%Y-%m-%d')
        if date_str not in daily_top_categories:
            daily_top_categories[date_str] = {
                'category': row['category'],
                'count': row['count']
            }
    
    list_data = [{
        "category": data['category'],
        "date": date,
        "count": data['count']
    } for date, data in daily_top_categories.items()]
    
    print('list_data',list_data)
    
    return JsonResponse({'data':list_data})

def otherData(request):
    return render(request, 'table_otherData.html')

def realtime_clickData(request):
    clickResult = Clickresult_Sparkstream.objects.all()
    data = [obj.to_dict() for obj in clickResult]
    return JsonResponse({'data':data})

def realtime_searchData(request):
    searchData = SearchResult_Sparkstream.objects.all()
    data = [obj.to_dict() for obj in searchData]
    return JsonResponse({'data':data})

def realtime_cartData(request):
    cartData = Cartresult_Sparkstream.objects.all()
    data = [obj.to_dict() for obj in cartData]
    return JsonResponse({'data':data})

def realtime_orderData(request):
    orderData = Orderesult_Sparkstream.objects.all()
    data = [obj.to_dict() for obj in orderData]
    return JsonResponse({'data':data})