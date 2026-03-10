from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Product, Comment

@login_required
def add_comment(request, product_id):
    if request.method == 'POST':
        comment_content = request.POST.get('comment')
        product = get_object_or_404(Product, id=product_id)
        
        if product:
            Comment.objects.create(
                user=request.user,
                product=product,
                content=comment_content
            )
            messages.success(request, '评论已成功提交！')
        else:
            messages.error(request, '产品不存在，无法提交评论。')
            
        return redirect('product_detail', id=product_id)