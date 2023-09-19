from django.contrib import admin
from django.utils.html import format_html
from .models import EmployeeInfo
from django.utils import timezone

class EmployeeInfoAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'email', 'first_name', 'last_name', 'employee_type')
    list_filter = ('employee_type', 'estado_civil', 'genero')
    search_fields = ('email', 'first_name', 'last_name', 'cpf', 'cnpj')
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    ordering = ['created_at']
    date_hierarchy = 'created_at'

    def image_tag(self, obj):
        if obj.image:  # Altere de obj.employee.image para obj.image
            return format_html('<img src="{0}" style="width: 40px;"/>'.format(obj.image.url))
        return "Sem imagem"
    image_tag.short_description = 'Image'



    def get_queryset(self, request):
        queryset = super(EmployeeInfoAdmin, self).get_queryset(request)
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

    class Media:
        js = ('employee_management/scripts.js',)

admin.site.register(EmployeeInfo, EmployeeInfoAdmin)
