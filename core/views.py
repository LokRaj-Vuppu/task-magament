from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.utils.email_service import EmailService
from core.models import Task
from core.serializers import (
    CreateTaskRequestValidationSerializer,
    DeleteTaskRequestValidationSerializer,
    TaskSerializer,
    UpdateTaskRequestValidationSerializer,
)


def home(request):
    return render(request, "core/index.html")


class GetAllTasks(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            print(f"Request Data - {request.data}")
            tasks = Task.objects.filter(user=request.user)
            tasks_serialized = TaskSerializer(tasks, many=True).data
            return Response(
                {"message": "Fetched All tasks", "tasks": tasks_serialized},
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            print(f"Exception in GetAllTasks API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CreateTask(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            print(f"Request - {request.data}")
            request_data = CreateTaskRequestValidationSerializer(data=request.data)
            if request_data.is_valid():
                title = request_data.validated_data["title"]
                description = request_data.validated_data.get("description")
                priority = request_data.validated_data.get("priority")
                task_status = request_data.validated_data.get("status")

                # Create Task
                try:
                    Task.objects.get(title=title, user=request.user)
                    return Response(
                        {"message": "Task already exists with given title"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except Task.DoesNotExist:
                    # setup celery and send email to the user
                    task = Task.objects.create(
                        title=title,
                        user=request.user,
                        description=description,
                        priority=priority,
                        status=task_status,
                    )

                # Email trigger from Celery
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
                        "dashboard_url": "http://localhost:8000/tasks/get/",
                    },
                )
                return Response(
                    {"message": "Task is created"}, status=status.HTTP_201_CREATED
                )

                # task_details , created = Task.objects.get_or_create(title=title, user=request.user,
                #                         description=description,
                #                         priority=priority, status=task_status)
                # if created:
                #     return Response({'message': 'Task is created'}, status=status.HTTP_201_CREATED)
                # return Response({'message': 'Task already exists with given title'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"message": "Invalid Request Data", "errors": request_data.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as error:
            print(f"Exception in CreateTask API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateTask(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        try:
            print(f"Request Data - {request.data}")
            request_data = UpdateTaskRequestValidationSerializer(
                data=request.data, partial=True
            )
            if request_data.is_valid():
                task_uuid = request_data.validated_data.get("task_uuid")

                try:
                    task = Task.objects.get(uuid=task_uuid)
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
                        "dashboard_url": "http://localhost:8000/tasks",
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
            print(f"Exception in UpdateTask API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteTask(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            print(f"Request Data - {request.data}")
            request_data = DeleteTaskRequestValidationSerializer(data=request.data)
            if request_data.is_valid():
                task_uuid = request_data.validated_data.get("task_uuid")
                try:
                    task = Task.objects.get(uuid=task_uuid)
                    email_context = {
                        "name": request.user.full_name or "Customer",
                        "task_title": task.title,
                        "task_description": task.description,
                        "priority": task.priority,
                        "status": task.status,
                        "dashboard_url": "http://localhost:8000/tasks",
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
            print(f"Exception in UpdateTask API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
