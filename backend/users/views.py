from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth.hashers import make_password
import requests
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Déconnexion réussie'}, status=200)


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
    


class Redirect42View(APIView):
    """
    Vue qui redirige l'utilisateur vers l'URL de connexion 42.
    """
    def get(self, request):
        api_42_auth_url = "https://api.intra.42.fr/oauth/authorize"
        params = {
            'client_id': settings.API_42_CLIENT_ID,
            'redirect_uri': settings.API_42_REDIRECT_URI,
            'response_type': 'code',
            'scope': 'public'
        }
        auth_url = f"{api_42_auth_url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type={params['response_type']}&scope={params['scope']}"
        return redirect(auth_url)


class Callback42View(APIView):
    def get(self, request):
        code = request.GET.get('code')

        if not code:
            return Response({'error': 'Code manquant dans la réponse de 42'}, status=status.HTTP_400_BAD_REQUEST)

        # Échanger le code contre un token d'accès
        token_url = "https://api.intra.42.fr/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.API_42_CLIENT_ID,
            'client_secret': settings.API_42_CLIENT_SECRET,
            'code': code,
            'redirect_uri': settings.API_42_REDIRECT_URI,
        }
        token_response = requests.post(token_url, data=data)

        if token_response.status_code != 200:
            return Response({'error': 'Impossible d’obtenir le token'}, status=token_response.status_code)

        token = token_response.json().get('access_token')

        # Obtenir les informations utilisateur
        user_info_url = "https://api.intra.42.fr/v2/me"
        user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {token}'})

        if user_info_response.status_code != 200:
            return Response({'error': 'Impossible d’obtenir les informations utilisateur'}, status=user_info_response.status_code)

        user_info = user_info_response.json()
        username = user_info.get('login')
        email = user_info.get('email')

        # Créer ou récupérer l'utilisateur dans la base de données
        user, created = CustomUser.objects.get_or_create(username=username, defaults={'email': email})

        # Connecter l'utilisateur et rediriger vers l'index
        login(request, user)
        return redirect('http://127.0.0.1:5500/frontend/index.html')  # Redirige vers l'URL d'accueil

    

class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({'username': user.username, 'email': user.email})
    


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Connecte l'utilisateur à la session

            # Générer un token d'authentification (par exemple avec JWT)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': f'Bienvenue, {user.username}!',
                'username': user.username,
                'email': user.email,
                'access_token': access_token  # Renvoie le token d'accès
            }, status=200)

        else:
            return Response({'error': 'Nom d’utilisateur ou mot de passe incorrect.'}, status=401)
