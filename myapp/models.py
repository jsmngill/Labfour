from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

#Name field:
class Type(models.Model):
    name = models.CharField(max_length=200)
    #adding str methods
    def __str__(self):
        return self.name
class Item(models.Model):
    type = models.ForeignKey(Type, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    # 2. adding the optional field of the description of the item requested
    description = models.TextField(null=True, blank=True)
    #adding str methods
    def __str__(self):
        return f"{self.name} - ${self.price}"
class Client(User):
    CITY_CHOICES = [
    ('WD', 'Windsor'),
    ('TO', 'Toronto'),
    ('CH', 'Chatham'),
    ('WL', 'WATERLOO'),]
    #fullname = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    # 4. Change default city value from Windsor to Chatham
    city=models.CharField(max_length=2, choices=CITY_CHOICES, default='CH')
    interested_in = models.ManyToManyField(Type)
    # 3. Add a phone number field that can be NULL
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # __str__ method
    def __str__(self):
        return self.username
#Question Updating Database Tables; OrderItem
class OrderItem(models.Model):
    # a. ForeignKey to Item table
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    # b. ForeignKey to Client table
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    # c. Field indicating number of items ordered
    quantity = models.PositiveIntegerField()

    # d. Status of the order with choices {0,1,2,3}
    STATUS_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Placed'),
        (2, 'Shipped'),
        (3, 'Delivered'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    # e. Date field indicating the last update date
    last_updated = models.DateTimeField(default=timezone.now)
    # __str__ method
    def __str__(self):
        return f"Order {self.id} by {self.client.username} for {self.quantity} {self.item.name}(s)"
    #Question7: adding the total price
    def total_price(self):
        return self.quantity * self.item.price

