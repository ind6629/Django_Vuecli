from django.contrib import admin
from .models import Cart
from .models import Cartresult_Sparkstream
from .models import Clickresult_Sparkstream
from .models import Collection
from .models import Comment
from .models import News
from .models import Order
from .models import Orderesult_Sparkstream
from .models import Product
from .models import SearchResult_Sparkstream
from .models import Track,TrackCart,TrackClick,TrackOrder,TrackSearch
from .models import User

admin.site.register(Cart)
admin.site.register(Cartresult_Sparkstream)
admin.site.register(Clickresult_Sparkstream)
admin.site.register(Collection)
admin.site.register(Comment)
admin.site.register(News)
admin.site.register(Order)
admin.site.register(Orderesult_Sparkstream)
admin.site.register(Product)
admin.site.register(SearchResult_Sparkstream)
admin.site.register(Track)
admin.site.register(TrackCart)
admin.site.register(TrackClick)
admin.site.register(TrackOrder)
admin.site.register(TrackSearch)
admin.site.register(User)
