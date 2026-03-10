from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from ..models import Order, Product
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from kafka import KafkaProducer
import json
import datetime


@require_http_methods(["GET"])
def load(request):
    # Get current user ID from session
    user_id = request.session.get('user_id', -1)
    orders = Order.objects.filter(user_id=user_id)
    return render(request, 'order.html', {'orders': orders})

@require_http_methods(["POST"])
def cancelOrder(request):
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        orders = Order.objects.filter(id__in=ids)
        count = orders.count()
        orders.delete()
        
        messages.success(request, "所选订单内容已成功移除")
        return JsonResponse({
            'success': True,
            'message': f'成功删除{count}个订单'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@require_http_methods(["POST"])
def settleOrder(request):
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        
        orders = Order.objects.filter(id__in=ids)
        totalPrice = sum(int(order.total_price) for order in orders)
        count = orders.count()
        orders.delete()
        
        messages.success(request, "所选订单内容已成功计算")
        return JsonResponse({
            'success': True,
            'message': f'成功结算{count}个订单,总价为：{totalPrice}'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
        
@csrf_exempt
def order(request,userId):
    orders = Order.objects.filter(user_id=userId)
    
    product_ids = [order.product_id for order in orders]
    products = Product.objects.filter(id__in=product_ids)
    product_map = {p.id: p for p in products}  
    
    order_data = [
        {
            "id": order.id,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "product": {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "image": product.image
            } if (product := product_map.get(order.product_id)) else None
        }
        for order in orders
    ]
    
    
    # bootstrap_servers = ['hadoop01:9092', 'hadoop02:9092', 'hadoop03:9092']
    # producer = KafkaProducer(
    # bootstrap_servers=bootstrap_servers,
    # value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
    # )
    # testOrders = Order.objects.all();
    # for order in testOrders:
    #     formatted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     tempProduct = Product.objects.filter(id = order.product_id).first();
    #     producer.send('order', {'user_id':order.user_id,'product_id':order.product_id,'category':tempProduct.category,'timestamp':order.timestamp.strftime('%Y-%m-%d %H:%M:%S')});
    #     print('add')
    # producer.flush()
        
        
    
    return JsonResponse(order_data, safe=False)  