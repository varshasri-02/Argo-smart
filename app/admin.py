from django.contrib import admin
from .models import *

# Register your models here.

class VisitorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Visitor, VisitorAdmin)

class AdminAdmin(admin.ModelAdmin):
    pass
admin.site.register(Admin, AdminAdmin)