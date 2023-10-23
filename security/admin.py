from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
from .models import CustomUser, RecoverPassword

admin.site.unregister(Group)
CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = ('profile_image', 'email', 'phone_number', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',)
    list_filter = ('email', 'is_active', 'is_staff', 'is_superuser',)
    search_fields = ('email', 'first_name', 'last_name', 'is_staff',)
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    ordering = ('-id',)

    class Media:
            css = {'all': ('security/style.css',)}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'image', 'bio', 'birthday', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Security', {'fields': ('failed_login_attempts', 'last_failed_login')})  # Adicionado essa seção
    )

    def profile_image(self, obj):
        if obj.image:
            image_url = obj.image.url
            return mark_safe(f'<img src="{image_url}" class="admin-profile-image" />')
        else:
            return '(Sem imagem)'
    profile_image.short_description = 'Imagem do Perfil'

    def phone_number(self, obj):
        return obj.phone_number
    phone_number.short_description = 'Número de Telefone'

    def save_model(self, request, obj, form, change):
        obj.username = obj.email
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.image:
            obj.image.delete()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.image:
                obj.image.delete()
        super().delete_queryset(request, queryset)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(RecoverPassword)
class RecoverPasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'token', 'expiry_datetime', 'is_used', 'ip_address')
    # readonly_fields = ['created_at', 'updated_at', 'deleted_at', 'otp', 'token', 'expiry_datetime', 'is_used', 'ip_address']
    list_filter = ('user', 'is_used', 'expiry_datetime')
    search_fields = ('user__email', 'otp', 'token') 

