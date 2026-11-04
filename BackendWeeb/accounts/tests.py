from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
# test pour vérifier que la page d'accueil est accessible

#creer un utilisateur pour les tests
User = get_user_model()

# `TestCase` → met en place une base de données de test jetable, recréée avant chaque test.
class AccountsAuthAPITests(APITestCase):

    def setUp(self):
        """
        Prépare un environnement de base propre exécuté AVANT chaque test.
        """
        # Données de base réutilisées pour les tests
        self.signup_url = reverse("signup")
        self.signin_url = reverse("signin")
        self.current_user_url = reverse("current_user")

        self.user_password = "testpassword"
        self.user_data = {
            "first_name": "Mounira",
            "last_name": "Iratni",
            "email": "testuser@exemple.com",
            "password": self.user_password,
        }

        self.active_user = User.objects.create_user(
            email="activeuser@exemple.com",
            first_name="Active",
            last_name="User",
            password=self.user_password,
            is_active=True
        )

    """
        Tests Inscription 
    """

    def test_signup_success(self):

        """
           verifie que linscription d'un nouvel utilisateur fonctionne et retourne 201 Created
        """

        response = self.client.post(self.signup_url, self.user_data, format="json")
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_signup_existing_email(self):
        """
           Vérifie qu'on ne peut pas créer deux comptes avec le même email.
        """

        duplicate_data = {
            "first_name": "Autre",
            "last_name": "Personne",
            "email": "activeuser@exemple.com",
            "password": "autrepassword123!",
        }

        response = self.client.post(self.signup_url, duplicate_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
        Tests Connexion
    """

    def test_signin_success(self):
        """
           Vérifie qu'un utilisateur actif recoit bien ses tokens JWT lors de la connexion et retourne 200 OK   
        """ 

        credentials = {
            "email": self.active_user.email,
            "password": self.user_password,
        }

        response = self.client.post(self.signin_url, credentials, format="json")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def test_signin_wrong_password(self):
        """
           Vérifie qu'un utilisateur ne peut pas se connecter avec un mot de passe incorrect et retourne 401 Unauthorized
        """

        credentials = {
            "email": self.active_user.email,
            "password": "wrongpassword",
        }

        response = self.client.post(self.signin_url, credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)