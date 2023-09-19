# signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(pre_save, sender=User)
def update_username_from_email(sender, instance, **kwargs):
    """"
    Verifique se o usuário já existe no banco de dados
    """
    if instance.pk:
        existing_user = User.objects.get(pk=instance.pk)
        
        if existing_user.email != instance.email:
            instance.username = instance.email



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Cria ou atualiza o perfil do usuário quando um usuário é criado ou atualizado.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(pre_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """
    Exclui o perfil do usuário quando o usuário é excluído.
    """
    try:
        instance.profile.delete()
    except Profile.DoesNotExist:
        pass
