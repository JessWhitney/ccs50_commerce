from django.contrib import admin
from .models import Categories, Bids, Listings, Comments

# Register your models here.
admin.site.register(Categories)
admin.site.register(Bids)
admin.site.register(Listings)
admin.site.register(Comments)
