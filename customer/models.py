# customer/models.py
from django.db import models
from datetime import date
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date_of_register = models.DateField(default=timezone.now)
    date_of_collection = models.DateField()
    amount_charged = models.FloatField()
    amount_paid = models.FloatField(default=0, blank=True, null=True)
    balance = models.FloatField(default=0, blank=True, null=True)
    total_sets = models.PositiveIntegerField(default=0)
    shirt_length = models.FloatField(default=0, blank=True, null=True)
    trouser_length = models.FloatField(default=0, blank=True, null=True)
    shoulder = models.FloatField(default=0, blank=True, null=True)
    sleeve = models.FloatField(default=0, blank=True, null=True)
    armhole = models.FloatField(default=0, blank=True, null=True)
    biceps = models.FloatField(default=0, blank=True, null=True)
    wrist = models.FloatField(default=0, blank=True, null=True)
    bust = models.FloatField(default=0, blank=True, null=True)
    waist = models.FloatField(default=0, blank=True, null=True)
    lap = models.FloatField(default=0, blank=True, null=True)
    stamina = models.FloatField(default=0, blank=True, null=True)
    ankle = models.FloatField(default=0, blank=True, null=True)
    neck = models.FloatField(default=0, blank=True, null=True)
    links = models.FloatField(default=0, blank=True, null=True)
    freehand = models.FloatField(default=0, blank=True, null=True)


    def __str__(self):
        return self.name


    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('due', 'Due'),
        ('paid', 'Paid'),
        ('completed', 'Completed'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    description = models.TextField()

    # ... (other methods or fields)

    def update_status(self):
        print(f"Date of Collection: {self.date_of_collection}")
        print(f"Balance: {self.balance}")
        print(f"Amount Paid: {self.amount_paid}")

        if self.date_of_collection < timezone.now().date() and self.balance == 0 and self.amount_paid == self.amount_charged:
            print("Condition 1 met")
            self.status = 'paid & completed'
        elif self.amount_charged == self.amount_paid and self.date_of_collection > timezone.now().date():
            print("Condition 2 met")
            self.status = 'paid & waiting'
        elif self.amount_charged != self.amount_paid and self.date_of_collection < timezone.now().date():
            print("Condition 3 met")
            self.status = 'due & completed'
        elif self.amount_charged != self.amount_paid and self.date_of_collection > timezone.now().date():
            print("Condition 4 met")
            self.status = 'due & waiting'

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)


class Image(models.Model):
    customer = models.ForeignKey('Customer', related_name='pictures', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='customer_pictures/', blank=True, null=True)
    pictures = models.ManyToManyField('self', blank=True)



   
    
