from django.db.models import QuerySet
from station_admin.models.site import Site


class SiteRepository:
    def find_with_rent_configured(self) -> QuerySet:
        return Site.objects.exclude(rent_charge_rule=None)
