from rest_framework import views
from rest_framework.response import Response

from .serializers import GetScoreSerializer, ScoreSerializer


class GetScoreView(views.APIView):
    """
    POST get_score/
    """

    def post(self, request):
        serializer = GetScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(ScoreSerializer(serializer.calculate_score()).data)
