from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
from .models import Profile, RecoverPassword

User = get_user_model()
admin.site.unregister(User) 
admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('profile_image', 'email', 'phone_number', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',)
    list_select_related = ('profile',)
    list_filter = ('email', 'is_active', 'is_staff', 'is_superuser',)
    search_fields = ('email', 'first_name', 'last_name', 'is_staff',)
    readonly_fields = ('username', 'date_joined', 'last_login', 'profile_image')
    ordering = ('-date_joined',)

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
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

    def profile_image(self, obj):
        if obj.profile.image:
            image_url = obj.profile.image.url
            return mark_safe(f'<img src="{image_url}" class="admin-profile-image" />')
        else:
            return '(Sem imagem)'
        
    def phone_number(self, obj):
        return obj.profile.phone_number
    phone_number.short_description = 'Phone Number'

    def save_model(self, request, obj, form, change):
        obj.username = obj.email
        super().save_model(request, obj, form, change)
        if 'profile' in form.changed_data:
            profile = form.cleaned_data['profile']
            profile.save()


    def delete_model(self, request, obj):
        if obj.profile.image:
            obj.profile.image.delete()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.profile.image:
                obj.profile.image.delete()
        super().delete_queryset(request, queryset)

admin.site.register(User, CustomUserAdmin)

@admin.register(RecoverPassword)
class RecoverPasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'token', 'expiry_datetime', 'is_used', 'ip_address')
