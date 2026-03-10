from django.shortcuts import render
from django.db.models import Count, Q
from django.http import JsonResponse
from datetime import datetime, timedelta
from ..models import TrackSearch, TrackCart, TrackOrder
import json

def init(request):
    return render(request, 'analysis.html')

def clickData(request):
    data = []
    return render(request, 'table_clickData.html', {'data': data})

def searchData(request):
    keywords_search_counts = TrackSearch.objects.values(
        'category'
    ).annotate(
        search_count=Count('id')
    )
    
    data = list(keywords_search_counts)
    print("---keywords_search_counts---")
    print(data)
    return render(request, 'table_searchData.html', {'data': data})

def cartData(request):
    cart_category_counts = TrackCart.objects.values(
        'category'
    ).annotate(
        count=Count('id')
    )
    
    data = list(cart_category_counts)
    print("---cart_category_counts---")
    print(data)
    return render(request, 'table_cartData.html', {'data': data})

def orderData(request):
    # Get current date and date 7 days ago
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Query most frequent category for each day in last 7 days
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

    # Extract top category for each day
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

    return render(request, 'table_orderData.html', {'data': list_data})

def otherData(request):
    return render(request, 'table_otherData.html')