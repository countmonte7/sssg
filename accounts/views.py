from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Order



@login_required
def profile(request):
    order_list = request.user.order_set.all()
    sum_amount = 0
    confirmed_order_list = []
    for order in order_list:
        order.update()
        if order.status == 'paid':
            confirmed_order_list.append(order)
            sum_amount += order.amount
    # order_list = Order.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {
        'order_list': confirmed_order_list,
        'sum_amount': sum_amount,
    })
