from django.contrib import admin
from .models import Master
admin.site.register(Master)
from .models import Category
admin.site.register(Category)
from .models import Rule
admin.site.register(Rule)

# Register your models here.
