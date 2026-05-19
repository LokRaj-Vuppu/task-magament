import logging

from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.utils.email_service import EmailService
from core.models import Task, TaskAttachment
from core.serializers import (
    CreateTaskRequestValidationSerializer,
    DeleteTaskRequestValidationSerializer,
    TaskSerializer,
    UpdateTaskRequestValidationSerializer,
)

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "core/index.html")


class GetAllTasks(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            tasks = Task.objects.filter(user=request.user)
            tasks_serialized = TaskSerializer(tasks, many=True).data
            return Response(
                {"message": "Fetched All tasks", "tasks": tasks_serialized},
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            logger.exception(f"Exception in GetAllTasks API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CreateTask(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            request_data = CreateTaskRequestValidationSerializer(data=request.data)
            if request_data.is_valid():
                title = request_data.validated_data["title"]
                description = request_data.validated_data.get("description")
                priority = request_data.validated_data.get("priority")
                task_status = request_data.validated_data.get("status")

                try:
                    Task.objects.get(title=title, user=request.user)
                    return Response(
                        {"message": "Task already exists with given title"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except Task.DoesNotExist:
                    task = Task.objects.create(
                        title=title,
                        user=request.user,
                        description=description,
                        priority=priority,
                        status=task_status,
                    )

                files = request.FILES.getlist("files")
                if files:
                    TaskAttachment.objects.bulk_create(
                        [TaskAttachment(task=task, file=file) for file in files]
                    )

                EmailService.send(
                    subject="🎉 Task Created Successfully",
                    recipient=request.user.email,
                    template_name="emails/task/create_task.html",
                    context={
                        "name": request.user.full_name or "Customer",
                        "task_title": task.title,
                        "task_description": task.description,
                        "priority": task.priority,
                        "status": task.status,
                        "dashboard_url": f"{settings.FRONTEND_BASE_URL}/tasks/get/",
                    },
                )
                return Response(
                    {"message": "Task is created"}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"message": "Invalid Request Data", "errors": request_data.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as error:
            logger.exception(f"Exception in CreateTask API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateTask(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        try:
            request_data = UpdateTaskRequestValidationSerializer(
                data=request.data, partial=True
            )
            if request_data.is_valid():
                task_uuid = request_data.validated_data.get("task_uuid")

                try:
                    task = Task.objects.get(uuid=task_uuid, user=request.user)
                except Task.DoesNotExist:
                    return Response(
                        {"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND
                    )

                for field, value in request_data.validated_data.items():
                    if field == "task_uuid":
                        continue

                    if value not in [None, ""]:
                        setattr(task, field, value)

                task.save()

                # Trigger Email After updating record via celery
                EmailService.send(
                    subject="✏️ Task Updated Successfully",
                    recipient=request.user.email,
                    template_name="emails/task/update_task.html",
                    context={
                        "name": request.user.full_name or "Customer",
                        "task_title": task.title,
                        "task_description": task.description,
                        "priority": task.priority,
                        "status": task.status,
                        "dashboard_url": f"{settings.FRONTEND_BASE_URL}/tasks",
                    },
                )

                return Response(
                    {"message": "Task updated Successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Invalid Request Data", "errors": request_data.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as error:
            logger.exception(f"Exception in UpdateTask API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteTask(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            request_data = DeleteTaskRequestValidationSerializer(data=request.data)
            if request_data.is_valid():
                task_uuid = request_data.validated_data.get("task_uuid")
                try:
                    task = Task.objects.get(uuid=task_uuid, user=request.user)
                    email_context = {
                        "name": request.user.full_name or "Customer",
                        "task_title": task.title,
                        "task_description": task.description,
                        "priority": task.priority,
                        "status": task.status,
                        "dashboard_url": f"{settings.FRONTEND_BASE_URL}/tasks",
                    }

                    task.delete()

                    EmailService.send(
                        subject="🗑️ Task Deleted Successfully",
                        recipient=request.user.email,
                        template_name="emails/task/delete_task.html",
                        context=email_context,
                    )
                except Task.DoesNotExist:
                    return Response(
                        {"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND
                    )

                return Response(
                    {"message": "Task Deleted Successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Invalid Request Data", "errors": request_data.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as error:
            logger.exception(f"Exception in DeleteTask API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
