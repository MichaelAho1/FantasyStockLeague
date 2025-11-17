from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import generics
from api.serializer import LeaguesSerializer, StockSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from catalog.models import LeagueParticipant, Stock, UserLeagueStock, League
from api.apiUtils.utils import getCurrentOpponent, getUserWeeklyStockProfits, getOwnedStocks, getTotalStockValue
from api.apiUtils.joinLeague import join_league

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ViewAllStocks(generics.ListCreateAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()  
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        stocks = []
        for stock in Stock.objects.all():
            data = {
                "ticker":stock.ticker,
                "name":stock.name,
                "start_price":stock.start_price,
                "current_price":stock.current_price,
            }
            stocks.append(data)
        return Response(stocks)


class ViewAllOwnedStocks(generics.ListCreateAPIView):
    #serializer_class = UserLeagueStockSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, format=None):
        owned_stocks = getOwnedStocks(league_id, request.user)
        stocks = []

        for stock in owned_stocks:
            data = {
                "shares":stock.shares,
                "current_price":stock.stock.current_price,
                "start_price":stock.stock.start_price,
                "ticker":stock.stock.ticker,
                "name":stock.name,
            }
            stocks.append(data)
        return Response(stocks)

class ViewUserWeeklyProfits(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, format=None):
        stocks = getUserWeeklyStockProfits(league_id, request.user)
        return Response(stocks)

class ViewOpponentWeeklyProfits(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, format=None):
        stocks = getUserWeeklyStockProfits(league_id, getCurrentOpponent(league_id, request.user))
        return Response(stocks)
        
class LeagueView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    # Viewing Data in a league
    def get(self, request, league_id):
        current_league = League.objects.get(league_id=league_id)
        league_participants = LeagueParticipant.objects.get(League=current_league)
        leagueUserData = []
        for league_participant in league_participants:
            total_profit = 0
            for stock in getOwnedStocks(league_id, league_participant.user):
                total_profit += (stock.price_at_start_of_week - stock.stock.current_price) * stock.shares
            data = {
                "user":league_participant.user,
                "wins":league_participant.wins,
                "losses":league_participant.losses,
                "net_worth": getTotalStockValue(league_id, league_participant.user) + league_participant.current_balance,
                "weekly_profit": total_profit,
                # Still needs schedule
            }
            leagueUserData.append(data)
        return Response(leagueUserData)

class ViewAllLeagues(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = League.objects.all()
    serializer_class = LeaguesSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        if request.user.is_superuser:
            all_leagues = League.objects.all()
            leagues = []
            for league in all_leagues:
                league_serializer = LeaguesSerializer(league)
                # Check if superuser is a participant in this league
                participant = LeagueParticipant.objects.filter(
                    league=league,
                    user=user
                ).first()
                
                if participant:
                    # Superuser is a participant, show like normal user
                    data = {
                        "league": league_serializer.data,
                        "leagueAdmin": participant.leagueAdmin,
                        "isParticipant": True
                    }
                else:
                    # Superuser is not a participant, show as view-only
                    data = {
                        "league": league_serializer.data,
                        "leagueAdmin": False,
                        "isParticipant": False
                    }
                leagues.append(data)
            
            response_data = {
                "is_superuser": True,
                "leagues": leagues
            }
            return Response(response_data)

        else:
            current_leagues = LeagueParticipant.objects.filter(user=user).distinct()
            leagues = []
            for league_participant in current_leagues:
                league_serializer = LeaguesSerializer(league_participant.league)
                data = {
                    "league": league_serializer.data,
                    "leagueAdmin": league_participant.leagueAdmin,
                    "isParticipant": True
                }
                leagues.append(data)
            response_data = {
                "is_superuser": False,
                "leagues": leagues
            }
            return Response(response_data)
    
    def post(self, request, *args, **kwargs):
        serializer = LeaguesSerializer(data=request.data)
        if serializer.is_valid():
            league = serializer.save()
            LeagueParticipant.objects.create(
                league=league,
                user=request.user,
                current_balance=Decimal('10000.00'),  
                leagueAdmin=True
            )
            return Response(serializer.data, status=201)
        return Response({'errors': serializer.errors}, status=400)


class JoinLeagueView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            league_id = request.data.get('league_id')
            success, response_data, status_code = join_league(league_id, request.user)
            return Response(response_data, status=status_code)
        except Exception as e:
            import traceback
            print(f"Error joining league: {str(e)}")
            print(traceback.format_exc())
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)



# Buy stocks
# Sell stocks


