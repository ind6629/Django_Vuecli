from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from ..models import Product, Cart, Order, News, Collection, Track, TrackOrder, TrackSearch
import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods
from kafka import KafkaProducer

def index(request):
    # Get track results
    track_results = Track.objects.values('user_id', 'product_id')
    
    # Get products by type
    phones = Product.objects.filter(type='phone')
    computers = Product.objects.filter(type='computer')
    appliances = Product.objects.filter(type='appliances')
    components = Product.objects.filter(type='component')
    
    # Get user ID from session
    user_id = request.session.get('user_id', -1)
    Carts = Cart.objects.filter(user_id=user_id).select_related('product')
    news = News.objects.all()

    track_data = []
    matching_product_ids = []

    for track in track_results:
        product_ids = track['product_id'].split(',')
        for product_id in product_ids:
            product = Product.objects.filter(id=product_id).first()
            if product:
                track_data.append({
                    'product_id': product_id,
                    'user_id': track['user_id'],
                    'name': product.name,
                    'image': product.image,
                    'stock': product.stock,
                    'price': product.price
                })

    return render(request, 'home.html', {
        'phones': phones,
        'computers': computers,
        'appliances': appliances,
        'components': components,
        'track_data': track_data,
        'news': news,
        'matching_product_ids': matching_product_ids,
        'Carts': Carts
    })

def help(request):
    products = Product.objects.all()
    return JsonResponse([product.to_dict() for product in products], safe=False)

def about(request):
    return render(request, 'about.html')

def product_detail(request, productId):
    # product = get_object_or_404(Product, id=id)
    # user_id = request.session.get('user_id', -1)
    
    # is_collected = Collection.objects.filter(
    #     user_id=user_id,
    #     product_id=id
    # ).exists()
    
    # return render(request, 'product_detail.html', {
    #     'product': product,
    #     'user_id': user_id,
    #     'is_collected': is_collected
    # })
    products = Product.objects.filter(id=productId)
    return JsonResponse([product.to_dict() for product in products], safe=False)

def category(request):
    fixed_value = request.GET.get('fixed_value', '')
    products = Product.objects.filter(category__icontains=fixed_value)
    return render(request, 'home.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = float(request.POST.get('price'))
        image = request.POST.get('image')
        stock = int(request.POST.get('stock'))
        description = request.POST.get('description')

        Product.objects.create(
            name=name,
            price=price,
            image=image,
            stock=stock,
            description=description
        )
        
        messages.success(request, 'Product added successfully!')
        return redirect('index')

    return render(request, 'add_product.html')

def edit_product(request, product_id):
    return render(request, 'edit_product.html')

def checkout(request):
    user_id = request.session.get('user_id', -1)
    cart_items = Cart.objects.filter(user_id=user_id).select_related('product')
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Kafka producer setup would go here
    # producer = KafkaProducer(...)

    for cart_item in cart_items:
        total_price = cart_item.product.price * cart_item.quantity
        order = Order.objects.create(
            user_id=user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            total_price=total_price
        )
        
        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()
        
        cart_item.delete()
        
        TrackOrder.objects.create(
            user_id=user_id,
            product_id=product.id,
            category=product.category
        )
        
        # Kafka send would go here
        # formatted_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # producer.send(...)

    messages.success(request, 'Order placed successfully!')
    return redirect('index')

def addOrder(request):
    user_id = request.session.get('user_id', -1)
    product_id = request.GET.get('product_id', type=int)
    product_price = request.GET.get('product_price', type=float)
    quantity = request.GET.get('quantity', type=int)
    
    total_price = product_price * quantity
    Order.objects.create(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
        total_price=total_price
    )
    
    product = Product.objects.get(id=product_id)
    product.stock -= quantity
    product.save()
    
    # Kafka producer and send would go here
    
    return redirect('order:load')

def collect(request, user_id, product_id, is_collected):
    if is_collected == 'True':
        collection = Collection.objects.filter(
            user_id=user_id,
            product_id=product_id
        ).first()
        if collection:
            collection.delete()
    else:
        Collection.objects.create(
            product_id=product_id,
            user_id=user_id
        )
        messages.success(request, '商品收藏成功!')
    
    return product_detail(request, product_id)

#@ensure_csrf_cookie
@csrf_exempt
def products(request, productType):
    products = Product.objects.filter(type=productType)
    return JsonResponse([p.to_dict() for p in products], safe=False) 

@csrf_exempt
def news(request):
    news = News.objects.all();
    return JsonResponse([p.to_dict() for p in news], safe=False) 

@require_http_methods(["POST"])
@csrf_exempt
def search(request):
    try:
        searchKeyword = request.POST.get('searchKeyword');
        user_id = request.POST.get('user_id');

        products = Product.objects.filter(
                Q(name__icontains=searchKeyword) |
                Q(description__icontains=searchKeyword) |
                Q(type__icontains=searchKeyword) |
                Q(category__icontains=searchKeyword)
            )
        dict_data = [{
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'image': item.image,
            'stock': item.stock,
            'description': item.description,
            'type': item.type,
            'category': item.category
        } for item in products]
        print('dict_data',dict_data);
        #向Kafka传入数据
        bootstrap_servers = ['hadoop01:9092', 'hadoop02:9092', 'hadoop03:9092']
        producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
        )
        # 搜索数据埋点
        for itme in dict_data:
            #print(itme);
            trackSerach = TrackSearch.objects.create(
                product_id=itme['id'],
                user_id=user_id,
                category=itme['category']
            )
            #print("create")
            trackSerach.save();
            producer.send('search', {'user_id':user_id,'product_id':itme['id'],'category':itme['category']});
        producer.flush()
    except:
        return JsonResponse({"status":"fail"});
    
    #return render_template('searchResult.html',products=products,keyword = searchKeyword)
    return JsonResponse({"status":"success","products":dict_data})
