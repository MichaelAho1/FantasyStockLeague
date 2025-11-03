from django.contrib import admin

from .models import Stock, LeagueSetting, LeagueParticipant, UserLeagueStocks, LeagueSchedule

admin.site.register(Stock)
admin.site.register(LeagueSetting)
admin.site.register(LeagueParticipant)
admin.site.register(UserLeagueStocks)
admin.site.register(LeagueSchedule)
