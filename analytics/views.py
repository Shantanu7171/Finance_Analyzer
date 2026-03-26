from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import AnalyticsService

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = AnalyticsService.get_dashboard_data(request.user)
        return Response(data)

class RecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recommendations = AnalyticsService.get_recommendations(request.user)
        return Response({"recommendations": recommendations})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    data = AnalyticsService.get_dashboard_data(request.user)
    recommendations = AnalyticsService.get_recommendations(request.user)
    return render(request, 'dashboard.html', {
        'data': data,
        'recommendations': recommendations
    })
