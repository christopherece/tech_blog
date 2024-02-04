from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.TextField()
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name