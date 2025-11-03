from django.contrib import admin

from .models import Portfolio, Stock, LeagueSetting, LeagueParticipant

admin.site.register(Portfolio)
admin.site.register(Stock)
admin.site.register(LeagueSetting)
admin.site.register(LeagueParticipant)
