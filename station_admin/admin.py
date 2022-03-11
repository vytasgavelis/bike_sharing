from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Site
from .models import ParkingSpot
from .models.charge_rule import ChargeRule

admin.site.register(Site)
admin.site.register(ParkingSpot)
admin.site.register(ChargeRule)

# admin.site.unregister(Group)

# class ChargeRuleInline(admin.TabularInline):
#     model = ChargeRule

#@admin.register(Author)
# class SiteAdmin(admin.ModelAdmin):
#     inlines = [ChargeRuleInline]


# admin.site.register(Site, SiteAdmin)
