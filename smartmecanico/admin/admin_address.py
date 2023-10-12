from django.contrib import admin
from django import forms
from django.utils import timezone
from smartmecanico.models.address_model import Address
from security.models import CustomUser

class AddressAdminForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if not user:
            raise forms.ValidationError('É necessário selecionar um usuário.')
        return user

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    form = AddressAdminForm
    list_display = ('cep', 'logradouro', 'complemento', 'bairro', 'localidade', 'uf', 'user_column')
    search_fields = ['cep', 'user__email']  # Usar 'user__email' em vez de 'user__username'
    list_display_links = ('cep', 'user_column')
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    ordering = ['created_at']
    autocomplete_fields = ['user']

    def user_column(self, instance):
        return instance.user.email  # Usar instance.user.email em vez de instance.user.username
    user_column.short_description = 'User'

    class Media:
        js = ('address/scripts.js',)

    def get_queryset(self, request):
        queryset = super(AddressAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser and form.cleaned_data.get('user'):
            obj.user = form.cleaned_data.get('user')
        super().save_model(request, obj, form, change)

    def delete_selected(self, request, queryset):
        queryset.update(deleted_at=timezone.now())

    delete_selected.short_description = 'Marcar selecionados como deletados'
