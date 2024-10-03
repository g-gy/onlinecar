from django.contrib import admin
from order.models import order

class orderadmin(admin.ModelAdmin):
    list_display=["id","customer","driver","startlocation","endlocation","tolls","mark" ]
    list_display_links=["id"]

admin.site.register(order, orderadmin)
