from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from ..models import Product, Cart, TrackCart, Order, TrackOrder
from kafka import KafkaProducer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import JsonResponse
from django.db.models import F
from kafka import KafkaProducer
import datetime
import json

@require_POST
@csrf_exempt
def add_to_cart(request):    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user_id = request.POST.get('user_id')
        quantity = request.POST.get('quantity')
        
        product = Product.objects.filter(id = product_id).first();
        if not product:
            return JsonResponse({'status': 'fail','message':'商品不存在'}, status=405)

        product_stock = int(product.stock);
        curr_quantity = int(quantity);
        if(product_stock<curr_quantity):
            return JsonResponse({'status': 'fail','message':'商品库存不足'}, status=405)
        product.stock = (product_stock-curr_quantity);
        product.save();
        
        cart = Cart.objects.create(
            product_id = product_id,
            user_id = user_id,
            quantity = quantity
        )
        cart.save();
        
        #向Kafka传入数据
        bootstrap_servers = ['hadoop01:9092', 'hadoop02:9092', 'hadoop03:9092']
        producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'))
        producer.send('cart', {'product_id':product.id,'user_id':user_id,'category':product.category});
        
        #购物车数据埋点🐱
        product = Product.objects.filter(id = product_id).first();
        trackCart = TrackCart.objects.create(product_id = product_id,user_id = user_id,category = product.category);
        trackCart.save();
        
        messages.success(request, 'Added to cart successfully!')
        return JsonResponse({'status': 'success','message':'添加成功'})
    return JsonResponse({'status': 'fail','message':'请求非法'}, status=405)

@require_POST
@csrf_exempt
def add_to_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        user_id = request.POST.get('user_id')
        quantity = request.POST.get('quantity')
        
        product = Product.objects.filter(id = product_id).first();
        if not product:
            return JsonResponse({'status': 'fail','message':'商品不存在'}, status=405)

        product_stock = int(product.stock);
        curr_quantity = int(quantity);
        if(product_stock<curr_quantity):
            return JsonResponse({'status': 'fail','message':'商品库存不足'}, status=405)
        product.stock = (product_stock-curr_quantity);
        product.save();
        product_price = int(product.price);
        total_price = curr_quantity*product_price;
        
        order = Order.objects.create(
            product_id = product_id,
            user_id = user_id,
            quantity = quantity,
            total_price = total_price
        )
        order.save();
        
        product = Product.objects.filter(id = product_id).first();
        trackOrder = TrackOrder.objects.create(product_id = product_id,user_id = user_id,category = product.category);
        trackOrder.save();
        
        bootstrap_servers = ['hadoop01:9092', 'hadoop02:9092', 'hadoop03:9092']
        producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
        )
        formatted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        producer.send('order', {'user_id':user_id,'product_id':product_id,'category':product.category,'timestamp':formatted_time});
        producer.flush()
        
        print(request, 'Added to order successfully!')
        return JsonResponse({'status': 'success','message':'添加成功'})
    return JsonResponse({'status': 'fail','message':'请求非法'}, status=405)

@require_POST
@csrf_exempt
def checkout(request):
    try:
        user_id = request.POST.get('user_id');
        carts = Cart.objects.filter(user_id = user_id);
        
        bootstrap_servers = ['hadoop01:9092', 'hadoop02:9092', 'hadoop03:9092']
        producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
        )

        for cart in carts:
            product = Product.objects.filter(id = cart.product_id).first();
            total_price = int(cart.quantity) * int(product.price);
            order = Order.objects.create(
            product_id = cart.product_id,
            user_id = user_id,
            quantity = cart.quantity,
            total_price = total_price)
            
            trackOrder = TrackOrder.objects.create(product_id = cart.product_id,user_id = user_id,category = product.category);
            trackOrder.save();
            order.save();
            cart.delete();
            
            formatted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            producer.send('order', {'user_id':user_id,'product_id':cart.product_id,'category':product.category,'timestamp':formatted_time});
        producer.flush()
        
    except:
        print(request, 'Added to order failly!')
        return JsonResponse({'status': 'fail','message':'结算异常'})
    return JsonResponse({'status': 'success','message':'成功结算'})

@csrf_exempt
def cart(request, userId):
    # 1. 查询用户购物车
    carts = Cart.objects.filter(user_id=userId)
    
    # 2. 提取所有商品ID并批量查询
    product_ids = [cart.product_id for cart in carts]
    products = Product.objects.filter(id__in=product_ids)
    product_map = {p.id: p for p in products}  # 转为字典提高查找效率
    
    # 3. 构建纯字典响应
    cart_data = [
        {
            "id": cart.id,
            "quantity": cart.quantity,
            "product": {
                "id": product.id,
                "name": product.name,
                "price": float(product.price)  # 处理Decimal类型
            } if (product := product_map.get(cart.product_id)) else None
        }
        for cart in carts
    ]
    
    # 4. 直接返回字典列表（不带status字段）
    return JsonResponse(cart_data, safe=False)  # safe=False允许返回列表

@require_POST
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Removed from cart successfully!')
    return redirect(reverse('cart'))