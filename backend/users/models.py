from django.contrib.auth.models import AbstractUser # classe de base django pour personnaliser utilisateur
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image  # Bibliothèque Pillow pour manipuler les images

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    # Ajout des nouveaux champs
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    victories = models.PositiveIntegerField(default=0)
    defeats = models.PositiveIntegerField(default=0)
    tournaments_participated = models.PositiveIntegerField(default=0)
    tournaments_won = models.PositiveIntegerField(default=0)

    # Résolution des conflits avec les related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        """Surcharge de la méthode save pour redimensionner l'avatar."""
        super().save(*args, **kwargs)  # Sauvegarde initiale

        if self.avatar:  # Si un avatar est défini
            avatar_path = self.avatar.path
            try:
                img = Image.open(avatar_path)  # Ouvre l'image
                img = img.convert('RGB')  # Convertit en RGB si nécessaire

                # Redimensionne à 128x128 pixels
                img = img.resize((128, 128), Image.Resampling.LANCZOS)

                # Sauvegarde l'image redimensionnée
                img.save(avatar_path, format='JPEG', quality=90)
            except Exception as e:
                print(f"Erreur lors du traitement de l'avatar : {e}")

    def __str__(self):
        return self.username


