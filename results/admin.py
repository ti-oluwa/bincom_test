from django.contrib import admin

from .models import (
    AnnouncedLgaResults, AnnouncedPuResults, 
    AnnouncedStateResults, AnnouncedWardResults
)


admin.site.register(AnnouncedStateResults)
admin.site.register(AnnouncedLgaResults)
admin.site.register(AnnouncedWardResults)
admin.site.register(AnnouncedPuResults)
