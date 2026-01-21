from rest_framework.views import APIView
from rest_framework.response import Response
from core_engine.engine import run_agent

class ResearchAPIView(APIView):
    def post(self, request):
        goal = request.data.get("goal")

        result = run_agent(goal)  

        return Response(result)
