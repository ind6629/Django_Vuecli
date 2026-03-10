from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import TrackClick, Product
from collections import defaultdict
import numpy as np
import json

@csrf_exempt
def track_result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            curr_user_id = data.get('user_id')
            
            # Get all track clicks and prepare data
            track_clicks = TrackClick.objects.all()
            track_clicks_data = [
                {'user_id': item.user_id, 'product_id': item.event_id}
                for item in track_clicks
            ]
            
            # Get recommendations
            product_ids = recommend(track_clicks_data, curr_user_id)
            
            # Get product details for recommendations
            recommend_products = []
            for product_id in product_ids:
                try:
                    product = Product.objects.get(id=product_id)
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
            
            # Kafka producer code would go here (commented out)
            # producer = KafkaProducer(...)
            # producer.send(...)
            
            return JsonResponse({
                "status": "success",
                "data": recommend_products
            })
            
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    
    return JsonResponse({
        "status": "error",
        "message": "Method not allowed"
    }, status=405)

def recommend(data, curr_user_id):
    """
    Jaccard similarity based recommendation system
    Maintains the exact same logic as the original Flask version
    """
    # Build item-user inverted index
    item_users = defaultdict(set)
    for item in data:
        item_users[item['product_id']].add(item['user_id'])

    # Calculate Jaccard similarity matrix
    items = list(item_users.keys())
    n = len(items)
    sim_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                sim_matrix[i][j] = 1.0  # Diagonal is 1
            else:
                item_i = items[i]
                item_j = items[j]
                users_i = item_users[item_i]
                users_j = item_users[item_j]

                intersection = len(users_i & users_j)
                union = len(users_i | users_j)

                sim_matrix[i][j] = intersection / union if union > 0 else 0

    # Convert to item similarity dictionary
    item_sim = defaultdict(dict)
    for i in range(n):
        for j in range(n):
            item_sim[items[i]][items[j]] = sim_matrix[i][j]
    
    # Get user's historical interactions
    user_items = set()
    for item in data:
        if item['user_id'] == curr_user_id:
            user_items.add(item['product_id'])
    
    # Calculate recommendation scores
    scores = defaultdict(float)
    for interacted_item in user_items:
        for candidate_item, similarity in item_sim[interacted_item].items():
            if candidate_item not in user_items:  # Exclude already interacted items
                scores[candidate_item] += similarity
    
    # Sort by score and return recommended items
    recommend_result = sorted(scores.items(), key=lambda x: -x[1])
    recommend_items = [item for item, score in recommend_result]
    
    return recommend_items