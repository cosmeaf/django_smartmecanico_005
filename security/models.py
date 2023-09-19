import os
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
import uuid

User = get_user_model()
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile_pictures', filename)


def validate_bio_height(value):
    if len(value) > 500:
        raise ValidationError('A biografia deve ter no máximo 500 caracteres.')

    
class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Ultima Atualização', auto_now=True)
    deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'


class RecoverPassword(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    otp = models.CharField(max_length=6, validators=[MinLengthValidator(6), MaxLengthValidator(6)])
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    expiry_datetime = models.DateTimeField(db_index=True)
    is_used = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Recupera Senhas'

    def __str__(self):
        return self.user.email

    def is_token_used(self):
        return self.is_used

    
class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField('Biografia', max_length=500, blank=True, null=True, validators=[validate_bio_height])
    phone_number = models.CharField('Contato',max_length=15, blank=True, null=True)
    birth_date = models.DateField('Data Nascimento',null=True, blank=True)
    image = models.ImageField('Imagem Perfil', upload_to=get_file_path, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def delete_old_image(self):
        try:
            old_profile = Profile.objects.get(id=self.id)
            if old_profile.image and old_profile.image != self.image and os.path.isfile(old_profile.image.path):
                os.remove(old_profile.image.path)
        except Profile.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        self.delete_old_image()
        super().save(*args, **kwargs)

