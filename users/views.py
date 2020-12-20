from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import AddUser
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET', 'POST'])
@csrf_exempt
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes([AllowAny])
def add_user(request):
    if request.method == 'GET':
        users = AddUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':  # To add a new user.
        data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
            'job': request.data.get('job'),
            'age': request.data.get('age')
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes([AllowAny])
def update_delete_user(request, user_id):
    try:
        users = AddUser.objects.get(id=user_id)  # To get the user whose ID is entered.
    except AddUser.DoesNotExist:
        return Response({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(users)
        return Response(serializer.data)

    if request.method == 'PUT':  # Updating the user with new data.
        serializer = UserSerializer(users, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PATCH"])
@csrf_exempt
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes([AllowAny])
def patch_user(request, user_id):
    try:
        users = AddUser.objects.get(id=user_id)
    except AddUser.DoesNotExist:
        return Response({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(users)
        return Response(serializer.data)

    elif request.method == 'PATCH':  # Updating the user's new entered fields. Partial update.
        payload = json.loads(request.body)
        try:
            user_item = AddUser.objects.filter(id=user_id)
            user_item.update(**payload)
            users = AddUser.objects.get(id=user_id)
            serializer = UserSerializer(users)
            return Response({'users': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
