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
        try:
            # Get league and participant first
            try:
                league = League.objects.get(league_id=league_id)
                participant = LeagueParticipant.objects.get(league=league, user=request.user)
                current_balance = float(participant.current_balance)
            except League.DoesNotExist:
                return Response({'error': 'League not found'}, status=404)
            except LeagueParticipant.DoesNotExist:
                return Response({'error': 'You are not a participant in this league'}, status=404)
            
            # Get owned stocks
            owned_stocks = getOwnedStocks(league_id, request.user)
            stocks = []

            for stock in owned_stocks:
                try:
                    data = {
                        "shares": float(stock.shares),
                        "current_price": float(stock.stock.current_price),
                        "start_price": float(stock.stock.start_price),
                        "price_at_start_of_week": float(stock.price_at_start_of_week),
                        "ticker": stock.stock.ticker,
                        "name": stock.stock.name,
                    }
                    stocks.append(data)
                except Exception as e:
                    print(f"Error processing stock {stock.stock.ticker}: {str(e)}")
                    continue
            
            # Calculate total stock value
            total_stock_value = getTotalStockValue(league_id, request.user)
            total_stock_value_float = float(total_stock_value) if total_stock_value is not None else 0.0
            
            return Response({
                "stocks": stocks,
                "current_balance": current_balance,
                "total_stock_value": total_stock_value_float,
                "net_worth": total_stock_value_float + current_balance
            })
        except Exception as e:
            import traceback
            print(f"Error in ViewAllOwnedStocks: {str(e)}")
            print(traceback.format_exc())
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)


class GetStockInfoView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, ticker, format=None):
        try:
            league = League.objects.get(league_id=league_id)
            participant = LeagueParticipant.objects.get(league=league, user=request.user)
            stock = Stock.objects.get(ticker=ticker)
            
            # Get owned shares if any
            try:
                user_stock = UserLeagueStock.objects.get(
                    league_participant=participant,
                    stock=stock
                )
                owned_shares = float(user_stock.shares)
            except UserLeagueStock.DoesNotExist:
                owned_shares = 0
            
            return Response({
                'balance': float(participant.current_balance),
                'owned_shares': owned_shares,
                'current_price': float(stock.current_price)
            })
        except League.DoesNotExist:
            return Response({'error': 'League not found'}, status=404)
        except LeagueParticipant.DoesNotExist:
            return Response({'error': 'You are not a participant in this league'}, status=404)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=404)

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



class BuyStockView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            from api.apiUtils.buySellStock import buy_stock
            
            league_id = request.data.get('league_id')
            ticker = request.data.get('ticker')
            shares = request.data.get('shares')
            
            if not league_id or not ticker or not shares:
                return Response({'error': 'league_id, ticker, and shares are required'}, status=400)
            
            success, response_data, status_code = buy_stock(league_id, request.user, ticker, shares)
            return Response(response_data, status=status_code)
        except Exception as e:
            import traceback
            print(f"Error buying stock: {str(e)}")
            print(traceback.format_exc())
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)


class SellStockView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            from api.apiUtils.buySellStock import sell_stock
            
            league_id = request.data.get('league_id')
            ticker = request.data.get('ticker')
            shares = request.data.get('shares')
            
            if not league_id or not ticker or not shares:
                return Response({'error': 'league_id, ticker, and shares are required'}, status=400)
            
            success, response_data, status_code = sell_stock(league_id, request.user, ticker, shares)
            return Response(response_data, status=status_code)
        except Exception as e:
            import traceback
            print(f"Error selling stock: {str(e)}")
            print(traceback.format_exc())
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)


class GetParticipantScheduleView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, league_id, format=None):
        """Get the schedule for the current user in a specific league"""
        try:
            from datetime import date
            from catalog.views import get_participant_schedule
            
            league = League.objects.get(league_id=league_id)
            participant = LeagueParticipant.objects.get(league=league, user=request.user)
            
            # Get all matchups for this participant
            matchups = get_participant_schedule(participant)
            
            # Calculate current week if league has started
            current_week = None
            if league.start_date:
                today = date.today()
                if today >= league.start_date:
                    days_since_start = (today - league.start_date).days
                    current_week = min((days_since_start // 7) + 1, 7)  # Cap at 7 weeks
                    # If it's past the end date, use week 7
                    if league.end_date and today > league.end_date:
                        current_week = 7
            
            # Format matchups for response
            schedule_data = []
            for matchup in matchups:
                # Determine opponent
                if matchup.participant1 == participant:
                    opponent = matchup.participant2
                    is_participant1 = True
                else:
                    opponent = matchup.participant1
                    is_participant1 = False
                
                schedule_data.append({
                    'week_number': matchup.week_number,
                    'opponent_username': opponent.user.username,
                    'opponent_id': opponent.id,
                    'is_current_week': current_week is not None and matchup.week_number == current_week,
                    'winner_id': matchup.winner.id if matchup.winner else None,
                    'is_winner': matchup.winner == participant if matchup.winner else None,
                })
            
            return Response({
                'schedule': schedule_data,
                'current_week': current_week,
                'league_start_date': league.start_date.isoformat() if league.start_date else None,
                'league_end_date': league.end_date.isoformat() if league.end_date else None,
            }, status=200)
            
        except League.DoesNotExist:
            return Response({'error': 'League not found'}, status=404)
        except LeagueParticipant.DoesNotExist:
            return Response({'error': 'You are not a participant in this league'}, status=404)
        except Exception as e:
            import traceback
            print(f"Error getting participant schedule: {str(e)}")
            print(traceback.format_exc())
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)


class SetLeagueStartDateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, league_id, *args, **kwargs):
        """Set start date for a league (requires 8 participants and league admin)"""
        try:
            from datetime import timedelta
            
            league = League.objects.get(league_id=league_id)
            
            # Check if user is a participant and admin
            try:
                participant = LeagueParticipant.objects.get(league=league, user=request.user)
                if not participant.leagueAdmin:
                    return Response({'error': 'Only league admins can set the start date'}, status=403)
            except LeagueParticipant.DoesNotExist:
                return Response({'error': 'You are not a participant in this league'}, status=404)
            
            # Check if league has 8 participants
            participant_count = league.participant_count
            if participant_count < 8:
                return Response({
                    'error': f'League must have 8 participants before setting start date. Currently has {participant_count} participants.'
                }, status=400)
            
            # Get start_date from request
            start_date = request.data.get('start_date')
            if not start_date:
                return Response({'error': 'start_date is required'}, status=400)
            
            # Parse and set start date
            from datetime import datetime, date
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
            
            # Validate that the date is a Monday (0 = Monday in Python's weekday())
            if start_date_obj.weekday() != 0:
                return Response({'error': 'Start date must be a Monday'}, status=400)
            
            # Calculate the next Monday (or later if today is Monday)
            today = date.today()
            today_weekday = today.weekday()  # 0 = Monday, 6 = Sunday
            
            if today_weekday == 6:  # Sunday
                days_until_monday = 1
            elif today_weekday == 0:  # Monday
                days_until_monday = 7  # Next Monday
            else:  # Tuesday through Saturday
                days_until_monday = 8 - today_weekday
            
            next_monday = today + timedelta(days=days_until_monday)
            
            # Validate that the start date is the next Monday or later
            if start_date_obj < next_monday:
                return Response({
                    'error': f'Start date must be the next Monday ({next_monday.strftime("%Y-%m-%d")}) or later'
                }, status=400)
            
            # Set start and end dates
            league.start_date = start_date_obj
            league.end_date = start_date_obj + timedelta(weeks=7)
            league.save()
            
            # Create league schedule - this is mandatory when setting start date
            from catalog.views import create_league_schedule
            try:
                created_matchups = create_league_schedule(league)
                schedule_message = f'Schedule created successfully with {len(created_matchups)} matchups'
            except ValueError as e:
                # This should not happen since we already validated 8 participants
                # But if it does, return an error
                return Response({
                    'error': f'Failed to create league schedule: {str(e)}'
                }, status=400)
            except Exception as e:
                # Any other error creating schedule
                import traceback
                print(f"Error creating league schedule: {str(e)}")
                print(traceback.format_exc())
                return Response({
                    'error': f'Failed to create league schedule: {str(e)}'
                }, status=500)
            
            serializer = LeaguesSerializer(league)
            return Response({
                'message': 'Start date set successfully and league schedule created',
                'schedule_info': schedule_message,
                'league': serializer.data
            }, status=200)
            
        except League.DoesNotExist:
            return Response({'error': 'League not found'}, status=404)
        except Exception as e:
            import traceback
            print(f"Error setting league start date: {str(e)}")
            print(traceback.format_exc())
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

