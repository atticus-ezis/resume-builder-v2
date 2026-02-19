from celery.result import AsyncResult
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TaskResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = AsyncResult(task_id)
        if task.failed():
            result = str(task.result)
        elif task.ready():
            result = task.result
        else:
            result = None
        return Response(
            {"status": task.status, "result": result},
            status=status.HTTP_200_OK,
        )
