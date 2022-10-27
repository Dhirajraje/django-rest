# Create your views here.
from rest_framework import status

from .serializer import LoginSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    return Response({
        'id': request.user.id,
        'name': request.user.username,
        'email': request.user.email,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    user_res = UserSerializer(data=request.data)
    if user_res.is_valid():
        result = user_res.save()
        if result:
            return Response(user_res.data, status=status.HTTP_201_CREATED)
    return Response(user_res.errors, status=status.HTTP_400_BAD_REQUEST)
