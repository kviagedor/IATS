from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Location),
admin.site.register(Department),
admin.site.register(Employee),
admin.site.register(Category),
admin.site.register(ITAsset),