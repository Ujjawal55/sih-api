from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Doctor)
admin.site.register(models.Address)
admin.site.register(models.Opd)
admin.site.register(models.Inventory)
admin.site.register(models.Inventory_Items)
