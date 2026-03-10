from .cart import Cart
from .cartresult_sparkstream import Cartresult_Sparkstream
from .clickresult_sparkstream import Clickresult_Sparkstream
from .collection import Collection
from .comment import Comment
from .news import News
from .order import Order
from .orderesult_sparkstream import Orderesult_Sparkstream
from .product import Product
from .searchresult_sparkstream import SearchResult_Sparkstream
from .track import Track,TrackCart,TrackClick,TrackOrder,TrackSearch
from .user import User
from .avatar import Avatar
# 显式导入所有模型

__all__ = ['Cart', 'Product','Cartresult_Sparkstream','Clickresult_Sparkstream','Collection','Comment',
           'News','Order','Orderesult_Sparkstream','SearchResult_Sparkstream','Track','TrackCart','TrackClick',
           'TrackOrder','TrackSearch','User','Avatar']  # 可选但推荐