from django.urls import path
from .views import GetScoreView

app_name = 'score'

urlpatterns = [path('get_score/', GetScoreView.as_view(), name='get_score')]
