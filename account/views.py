from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView    
from account.serializers import UserManagerSerializers

class  UserRegistrationView(APIView):
    def post(self, request,format=None):
        serializer= UserManagerSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'msg':'Registration sucess'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)