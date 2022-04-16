from email import message
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from base.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def userSignup(request):
    name = request.data['name']
    username = request.data['username']
    password = request.data['password'] 
    try:
        User.objects.get(username=username)
        return Response({'status': False, 'error': 'Username already exists'})
    except:
        user = User.objects.create_user(first_name=name, username=username, password=password)
        user.save()
        return Response({'status': True, 'message': 'Account created successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userHome(request):
    tony = [
        'https://i.pinimg.com/564x/b6/55/8e/b6558ea02efd9abe75f18956a5b5c197.jpg',
        'https://i.pinimg.com/564x/51/33/1f/51331f0ee2951bafa0e43ec42a06df63.jpg',
        'https://i.pinimg.com/564x/66/88/c7/6688c783572759b1fbf2ab179ac2a3e3.jpg',
        'https://i.pinimg.com/564x/80/7b/55/807b5544b3cc60c7c315741b65cc5f83.jpg',
        'https://i.pinimg.com/564x/d4/80/e9/d480e9ec80da6e867cc3c04e00a55f44.jpg'

    ]
    return Response({'status': True,'data': tony})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addUser(request):
    if request.user.is_staff:
        name = request.data['name']
        username = request.data['username']
        password = request.data['password']
        user = User.objects.create_user(first_name=name, username=username, password=password)
        user.save()
        return Response({'status': True, 'message': 'User added successfully'})
    else:
        return Response({'status': False, 'error': 'You are not authorized to add users'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUser(request):
    if request.user.is_staff:
        users = User.objects.all()
        usersList = []
        for user in users:
            if user.is_staff == False:
                usersList.append({
                    'id': user.id,
                    'name': user.first_name,
                    'username': user.username,
                    'password': user.password,
                })
        return Response({'status': True, 'data':usersList})
    else:
        return Response({'status': False, 'error': 'You are not authorized to view details of users'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    if request.user.is_staff:
        User.objects.filter(id=request.data['id']).delete()
        users = User.objects.all()
        usersList = []
        for user in users:
            if user.is_staff == False:
                usersList.append({
                    'id': user.id,
                    'name': user.first_name,
                    'username': user.username,
                    'password': user.password,
                })
        return Response({'status': True, 'data':usersList})
    else:
        return Response({'status': False, 'error': 'You are not authorized to delete users'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    if request.user.is_staff:
        try:
            User.objects.get(username=request.data['username'])
            return Response({'status': False, 'error': 'Username already exists'})
        except:
            User.objects.filter(id=request.data['id']).update(first_name=request.data['name'], username=request.data['username'])
            return Response({'status': True, 'message': 'User updated successfully'})
    else:
        return Response({'status': False, 'error': 'You are not authorized to update users'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUserDetails(request):
    if request.user.is_staff:
        user = User.objects.get(id=request.data['id'])
        return Response({'status': True, 'data': {
            'id': user.id,
            'name': user.first_name,
            'username': user.username,
        }})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def isAdmin(request):
    if request.user.is_staff:
        return Response({'status': True})
    else:
        return Response({'status': False})