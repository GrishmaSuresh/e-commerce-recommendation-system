from django.db import models
from django.contrib.auth.models import User

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=100)
    product = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_id} → {self.product}"
