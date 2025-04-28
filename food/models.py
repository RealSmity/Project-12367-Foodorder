from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    image = models.CharField(max_length=2083)

class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='ผู้สั่งซื้อ')
    order_date = models.DateTimeField(default=timezone.now, verbose_name='วันที่สั่งซื้อ')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='ยอดรวม')
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'รอการยืนยัน'),
            ('processing', 'กำลังดำเนินการ'),
            ('shipping', 'กำลังจัดส่ง'),
            ('delivered', 'จัดส่งแล้ว'),
            ('cancelled', 'ยกเลิก'),
        ],
        default='pending',
        verbose_name='สถานะการจัดส่ง'
    )

    class Meta:
        verbose_name = 'คำสั่งซื้อ'
        verbose_name_plural = 'คำสั่งซื้อ'
        ordering = ['-order_date']  # เรียงตามวันที่สั่งซื้อล่าสุด

    def __str__(self):
        return f"Order #{self.order_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, verbose_name='จำนวน')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ราคาต่อหน่วย')

    def get_total_price(self):
        return self.quantity * self.price

    class Meta:
        verbose_name = 'รายการสั่งซื้อ'
        verbose_name_plural = 'รายการสั่งซื้อ'

    def __str__(self):
        return f"{self.food.name} x {self.quantity} ใน Order #{self.order.order_id}"