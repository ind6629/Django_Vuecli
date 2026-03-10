# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
import numpy as np
from ..models import TrackClick, Product
import json

@csrf_exempt
@require_http_methods(["POST"])
def recommend(request):
    try:
        # 1. 解析请求数据
        curr_user_id = request.POST.get('user_id');
        # 2. 获取所有点击记录
        track_clicks = TrackClick.objects.all()
        track_clicks_data = [
            {'user_id': item.user_id, 'product_id': item.product_id}
            for item in track_clicks
        ]
        
        #print('track_clicks_data',track_clicks_data)
        
        # 3. 执行推荐算法
        product_ids = process(track_clicks_data, curr_user_id)
        #print('product_ids',product_ids)
        # 4. 获取推荐商品详情
        recommend_products = []
        for product_id in product_ids:
            try:
                product = Product.objects.filter(id=product_id).first();
                recommend_products.append({
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'price': float(product.price),
                    'stock': product.stock,
                    'image': product.image,
                    'category': product.category
                })
            except Product.DoesNotExist:
                continue
        
        return JsonResponse({
            "status": "success",
            "data": recommend_products
        })
    
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

def process(data, curr_user_id):
    """基于Jaccard相似度的推荐算法"""
    # 构建物品-用户倒排表
    item_users = defaultdict(set)
    for item in data:
        item_users[item['product_id']].add(item['user_id'])

    # 计算Jaccard相似度矩阵
    items = list(item_users.keys())
    n = len(items)
    sim_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                sim_matrix[i][j] = 1.0
            else:
                users_i = item_users[items[i]]
                users_j = item_users[items[j]]
                intersection = len(users_i & users_j)
                union = len(users_i | users_j)
                sim_matrix[i][j] = intersection / union if union > 0 else 0

    # 构建相似度字典
    item_sim = {
        items[i]: {items[j]: sim_matrix[i][j] for j in range(n)}
        for i in range(n)
    }
    
    #print('item_sim',item_sim)
    
    # 获取用户历史交互物品
    # user_items = {
    #     item['product_id'] 
    #     for item in data 
    #     if item['user_id'] == curr_user_id
    # }

    user_items = set()
    for item in data:
        item_id = item['user_id'];
        #print("item_id",type(item_id),item_id);
        #print("curr_user_id",type(curr_user_id),curr_user_id);
        curr_user_id = int(curr_user_id)
        if item_id == curr_user_id:
            #print("add")
            user_items.add(item['product_id'])
    #print('user_items',user_items)

    
    # 计算推荐得分
    scores = defaultdict(float)
    for interacted_item in user_items:
        for candidate_item, similarity in item_sim.get(interacted_item, {}).items():
            if candidate_item not in user_items:
                scores[candidate_item] += similarity
    
    print(scores);
                
    
    
    # 按得分排序返回推荐商品ID
    return [
        item for item, score in 
        sorted(scores.items(), key=lambda x: -x[1])
    ]