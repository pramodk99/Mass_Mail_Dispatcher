from django.db import models

# class Signup(models.Model):
#     username = models.CharField( max_length=120, unique = True)
#     password = models.CharField( max_length=120)
#     def __str__(self):
#             return self.username

class GMail(models.Model):
    email = models.EmailField()
    def __str__(self):
        return self.email
    

