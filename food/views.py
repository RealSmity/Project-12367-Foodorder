from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Food, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
import uuid

@login_required(login_url='/login/')
def create_order(request):
    if request.method == 'POST':
        food_id = request.POST.get('food_id')
        quantity = int(request.POST.get('quantity', 1))
        food = get_object_or_404(Food, pk=food_id)

        order = Order.objects.create(
            user=request.user,
            order_date=timezone.now()  # ระบุเวลาปัจจุบันโดยอัตโนมัติ
        )

@staff_member_required
def all_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'all_orders.html', {'orders': orders})

@login_required
def search_orders_results(request):
    query = Q(user=request.user)  # เริ่มด้วยการ filter เฉพาะ user ปัจจุบัน
    order_id = request.GET.get('order_id')
    menu_item = request.GET.get('menu_item')
    status = request.GET.get('status')

    print(f"Order ID received: {order_id}")

    if order_id:
        try:
            uuid.UUID(order_id)
            query &= Q(order_id=order_id)
        except ValueError:
            pass
    if menu_item:
        query &= Q(items__food__name__icontains=menu_item)
    if status:
        query &= Q(status=status)

    results = Order.objects.filter(query).distinct().order_by('-order_date')
    return render(request, 'search_orders.html', {'results': results})

@login_required
def search_orders(request):
    return render(request, 'search_orders.html')

@login_required
@require_POST
def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    if order.status not in ['delivered', 'cancelled']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, f"คำสั่งซื้อ #{order.order_id} ถูกยกเลิกแล้ว.")
        return redirect('user_orders')
    else:
        messages.error(request, f"ไม่สามารถยกเลิกคำสั่งซื้อ #{order.order_id} ได้เนื่องจากอยู่ในสถานะ '{order.get_status_display}'.")
        return redirect('user_orders')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'user_orders.html', {'orders': orders})

@login_required(login_url='/login/') # ถ้ามีการใช้งานระบบล็อกอิน
def create_order(request):
    if request.method == 'POST':
        food_id = request.POST.get('food_id')
        quantity = int(request.POST.get('quantity', 1))
        food = get_object_or_404(Food, pk=food_id)

        order = Order.objects.create(user=request.user) # เชื่อมกับ User ที่ล็อกอิน
        OrderItem.objects.create(order=order, food=food, quantity=quantity, price=food.price)
        order.total_amount = food.price * quantity
        order.save()

        messages.success(request, f"สั่งซื้อ '{food.name}' จำนวน {quantity} รายการ สำเร็จ!")
        return redirect('home') # Redirect กลับไปหน้า Home หรือหน้าแสดง Order

    else:
        return HttpResponse("Method Not Allowed", status=405)
    
def home(request):
    food = Food.objects.all
    return render(request, 'home.html', {'food': food})
