from django.contrib import admin
from .models import *
from users.models import *

admin.site.register(Product)
admin.site.register(User)
admin.site.register(CartItem)
admin.site.register(Cart)