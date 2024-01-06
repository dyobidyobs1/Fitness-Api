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
from .utils import *

from random import randint


@api_view(['DELETE'])
def plan_delete(request, pk):
    plan = GeneratePlan.objects.get(id=pk)
    plan.delete()
    return Response({'delete': "Success"})


@api_view(['POST'])
def plan_delete(request):
    plan = GeneratePlan.objects.get(id=request.data['id'])
    plan.delete()
    return Response({'delete': "Success"})

@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, username=request.data['username'])
    if not user.check_password(request.data['password']) and user.is_verified:
         return Resopnse({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializerUser = UserSerializer(instance=user)
    stats, created = Stats.objects.get_or_create(user=user)
    stats = StatsSerializer(stats)
    return Response({'token': token.key, 'user': serializerUser.data, 'stats': stats.data})

@api_view(['POST'])
def register(request):
    serializerUser = UserSerializer(data=request.data)
    random_id = create_rand_id()
    print(serializerUser)
    if serializerUser.is_valid():
        serializerUser.save()
        user = CustomUser.objects.get(username=request.data['username'])
        print("user", user)
        user.set_password(request.data['password'])
        user.verification_token = random_id
        user.save()
        token = Token.objects.create(user=user)
        send_email_token(request.data['email'], random_id)
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
    serializerExercise =  ExcerciseSerializer(Exercise.objects.order_by('?')[:7], many=True)
    # for i in range(0, 10):
    #     if not serializerExercise.data in random_excercise:
    #         random_excercise.append(serializerExercise.data)
    #     if len(random_excercise) == 3:
    #         continue
    if serializerExercise:
        print(serializerExercise.data)
        return Response({"exercise" : serializerExercise.data})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def stats(request):
    stats, created = Stats.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        serializerExercise = StatsSerializer(instance=stats, data=request.data)
        print(serializerExercise)
        if serializerExercise.is_valid():
            serializerExercise.save()
            return Response({'stats': serializerExercise.data})
    else:
        serializerExercise =  StatsSerializer(stats)
        if serializerExercise:
            return Response({"stats" : serializerExercise.data})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializerExercise.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['POST', 'GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = CustomUser.objects.get(username=request.user.username)
    if request.method == 'POST':
        serializerUser = ProfileSerializer(instance=user, data=request.data)
        print(serializerUser)
        if serializerUser.is_valid():
            serializerUser.save()
            return Response({'user': serializerUser.data})
    else:
        serializerUser =  UserSerializer(instance=user)
        stats = Stats.objects.get(user=request.user)
        if serializerUser:
            levelup = StatsSerializer(stats)
            return Response({"profile" : serializerUser.data, "level": levelup.data['current_level']})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializerUser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def history(request):
    stats, created = Stats.objects.get_or_create(user=request.user)
    if request.method == 'POST' and not created:
        serializerHistory = HistorySerializer(data=request.data)
        print(serializerHistory)
        if serializerHistory.is_valid():
            done_excercise = serializerHistory.save(user=request.user)
            print(stats)
            current = stats.current_exp
            stats.current_exp = current + int(done_excercise.exp_gain)
            stats.level_up()
            stats.save()
            return Response({'user': serializerHistory.data})
        else:
            return Response(serializerHistory.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializerHistory =  HistorySerializer(History.objects.filter(user=request.user).order_by('-date_created'), many=True)
        if serializerHistory:
            return Response({"history" : serializerHistory.data})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def leaderboards(request):
    serializerExercise =  LeaderboardsSerializer(Stats.objects.order_by('-current_level'), many=True)
    # for i in range(0, 10):
    #     if not serializerExercise.data in random_excercise:
    #         random_excercise.append(serializerExercise.data)
    #     if len(random_excercise) == 3:
    #         continue
    if serializerExercise:
        return Response({"leaderboards" : serializerExercise.data})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST', 'GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def plangenerate(request):
    if request.method == 'POST':
        serializerGeneratedPlan = GenerarePlanSerializer(data=request.data)
        print(serializerGeneratedPlan)
        if serializerGeneratedPlan.is_valid():
            done_excercise = serializerGeneratedPlan.save(user=request.user)
            return Response({'generated': serializerGeneratedPlan.data})
        else:
            return Response(serializerGeneratedPlan.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializerGeneratedPlan =  GenerarePlanSerializer(GeneratePlan.objects.filter(user=request.user).order_by('-date_created'), many=True)
        if serializerGeneratedPlan:
            return Response({"generated" : serializerGeneratedPlan.data})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# Verify Code
@api_view(['POST'])
def verify(request):
    try:
        userDetails = CustomUser.objects.get(verification_token=request.data['verify_code'])
        userDetails.is_verified = True
        userDetails.save()
        return Response({'status': "true"}) 
    except Exception as e:
        return Response({'status': "false"})