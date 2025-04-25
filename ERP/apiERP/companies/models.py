from django.db import models

class Enterprise(models.Model):
    name = models.CharField(max_length=75)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)