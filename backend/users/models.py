from django.contrib.auth.models import AbstractUser # classe de base django pour personnaliser utilisateur
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    # Ajoutez des related_name pour résoudre les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Nom unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Nom unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username # retourne l'objet plus specigiquement son username

