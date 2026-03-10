from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from ..models import Collection, Product, TrackClick
from django.utils import timezone
from kafka import KafkaProducer
import json

@require_http_methods(["GET", "POST"])
@login_required
def load(request):
    # Get collections for current user
    collections = Collection.objects.filter(user=request.user).select_related('product')
    return render(request, 'collection.html', {'collections': collections})

@require_http_methods(["POST"])
@csrf_exempt
def remove(request):
    try:
        user_id = request.POST.get('user_id');
        product_id = request.POST.get('product_id');
        #print(user_id,product_id);
        collection = Collection.objects.filter(user_id = user_id,product_id = product_id).first();
        collection.delete();
    except:
        print("移除收藏操作异常")
        return JsonResponse({'status':'fail','message':'移除收藏操作异常'})  
    return JsonResponse({'status':'success','message':'移除收藏操作成功'}) 
        
def collections(request,userId):
    collections = Collection.objects.filter(user_id=userId);
    
    product_ids = [order.product_id for order in collections]
    products = Product.objects.filter(id__in=product_ids)
    product_map = {p.id: p for p in products}  
    
    collection_data = [
        {
            "id": collection.id,
            "user_id": collection.user_id,
            "product_id": collection.product_id,
            "product": {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "image": product.image,
                "stock": product.stock
            } if (product := product_map.get(collection.product_id)) else None
        }
        for collection in collections
    ]
    
    return JsonResponse(collection_data, safe=False)  

@require_http_methods(["POST"])
@csrf_exempt
def checkCollect(request):
    try:
        user_id = request.POST.get('user_id');
        product_id = request.POST.get('product_id');
        collection = Collection.objects.filter(user_id = user_id,product_id = product_id).first();
        
        #点击数据埋点
        product = Product.objects.filter(id = product_id).first();
        #print(product_id,user_id,product.category);
        trackClick = TrackClick.objects.create(product_id = product_id,user_id = user_id,category = product.category,event_type = 99 )
        trackClick.save();
        #向Kafka传入数据
        bootstrap_servers = ['hadoop01:9092', 'hadoop02:9092', 'hadoop03:9092']
        producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
        )
        producer.send('click', {'product_id':product_id,'user_id':user_id,'category':product.category});
        producer.flush()
        
        if not collection:
            return JsonResponse({'status': 'fail','message':'不存在该收藏记录'})
    except:
        return JsonResponse({'status': 'fail','message':'收藏记录查询异常'})
    return JsonResponse({'status': 'success','message':'用户已收藏'})

@require_http_methods(["POST"])
@csrf_exempt
def collect(request):
    try:
        user_id = request.POST.get('user_id');
        product_id = request.POST.get('product_id');
        #print(user_id,product_id);
        existRecord = Collection.objects.filter(user_id = user_id,product_id = product_id).first();
        if existRecord:
            return JsonResponse({'status':'success','message':'收藏记录已存在'}) 
        collection = Collection.objects.create(user_id = user_id,product_id = product_id);
        collection.save();
    except:
        print("添加收藏操作异常")
        return JsonResponse({'status':'fail','message':'添加收藏操作异常'})  
    return JsonResponse({'status':'success','message':'添加收藏操作成功'}) 