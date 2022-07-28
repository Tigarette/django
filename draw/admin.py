from django.contrib import admin
from django.contrib.auth.models import User
from .models import MyUser, DrawQuestion, DrawChoice

# Register your models here.


admin.site.register(DrawQuestion)
admin.site.register(DrawChoice)
admin.site.register(MyUser)
