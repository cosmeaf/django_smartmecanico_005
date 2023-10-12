import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, MaxLengthValidator


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile_pictures', filename)

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)
    deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True)

    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(Base, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField('Imagem Perfil', upload_to=get_file_path, null=True, blank=True)
    bio = models.TextField('Biografia', max_length=500, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Cliente / Usuário"
        verbose_name_plural = "Clientes / Usuários"

    def __str__(self):
        return self.email

    def delete_old_image(self):
        try:
            old_profile = CustomUser.objects.get(id=self.id)
            if old_profile.image and old_profile.image != self.image and os.path.isfile(old_profile.image.path):
                os.remove(old_profile.image.path)
        except CustomUser.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        self.delete_old_image()
        super().save(*args, **kwargs)


class RecoverPassword(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_index=True)
    otp = models.CharField(max_length=6)
    token = models.UUIDField(unique=True)
    expiry_datetime = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()
    browser = models.CharField(max_length=255, null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)
    os_name = models.CharField(max_length=255, null=True, blank=True)
    os_version = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Recuperar Senha'
        verbose_name_plural = 'Recupera Senhas'

    def __str__(self):
        return self.user.email

    def is_token_used(self):
        return self.is_used
