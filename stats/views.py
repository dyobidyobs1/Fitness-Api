from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import *
from .models import *

from random import randint


@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, username=request.data['username'])
    if not user.check_password(request.data['password']):
         return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializerUser = UserSerializer(instance=user)
    return Response({'token': token.key, 'user': serializerUser.data})

@api_view(['POST'])
def register(request):
    serializerUser = UserSerializer(data=request.data)
    print(serializerUser)
    if serializerUser.is_valid():
        serializerUser.save()
        user = CustomUser.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializerUser.data})
    return Response(serializerUser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed! {}".format(request.user.username))


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def exercise(request):
    random_excercise = []
    serializerExercise =  ExcerciseSerializer(Exercise.objects.order_by('?')[:3], many=True)
    # for i in range(0, 10):
    #     if not serializerExercise.data in random_excercise:
    #         random_excercise.append(serializerExercise.data)
    #     if len(random_excercise) == 3:
    #         continue
    if serializerExercise:
        return Response({"exercise" : serializerExercise.data})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
