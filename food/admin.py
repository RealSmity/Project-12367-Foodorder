from django.contrib import admin
from .models import Food, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # จำนวน Form ว่างที่จะแสดง

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'order_date', 'total_amount', 'status')
    list_filter = ('status', 'order_date', 'user')
    inlines = [OrderItemInline]

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'image') # ตัวอย่างการปรับแต่ง
    # เพิ่ม filter, search fields หรืออื่นๆ ได้ตามต้องการ