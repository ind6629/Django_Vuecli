from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import TrackClick
import json

@csrf_exempt
def track_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_id = data.get('event_id')
            event_type = data.get('event_type')
            user_id = data.get('user_id')
            category = data.get('category')
            
            # -1 is visitor ID
            if user_id == -1:
                return JsonResponse({"status": "success"})
            
            # Create and save TrackClick record
            TrackClick.objects.create(
                event_id=event_id,
                event_type=event_type,
                user_id=user_id,
                category=category,
            )
            
            # Kafka producer setup would go here
            # producer = KafkaProducer(...)
            # producer.send('click', {
            #     'product_id': event_id,
            #     'user_id': user_id,
            #     'category': category
            # })
            # producer.flush()
            
            return JsonResponse({"status": "success"})
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)