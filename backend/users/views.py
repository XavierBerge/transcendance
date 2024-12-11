from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class SignupView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Ce pseudo est déjà utilisé.'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Cette adresse email est déjà utilisée.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create(username=username, email=email, password=make_password(password))
        return Response({'message': 'Utilisateur créé avec succès'}, status=status.HTTP_201_CREATED)
