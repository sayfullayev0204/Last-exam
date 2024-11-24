from django.contrib import admin
from .models import UserModel, Admin, Customer

admin.site.register(UserModel)
admin.site.register(Admin)
admin.site.register(Customer)
