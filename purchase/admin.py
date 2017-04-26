from django.contrib import admin
from purchase.models import PurchaseIndentRequest, Item, Vendor

# Register your models here.
admin.site.register(PurchaseIndentRequest)
admin.site.register(Item)
admin.site.register(Vendor)
