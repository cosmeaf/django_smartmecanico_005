from django.contrib import admin
from smartmecanico.models.services_model import HourService

@admin.register(HourService)
class HourServiceAdmin(admin.ModelAdmin):
    list_display = ('hour', 'user_email')
    ordering = ['created_at']
    search_fields = ['hour', 'user__email'] 
    exclude = ['user', ]
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']

    def get_queryset(self, request):
        """
        Show result user by id
        """
        queryset = super(HourServiceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user_id=request.user.id)

    def user_email(self, obj):
        return obj.user.email 
    user_email.short_description = 'User Email'

    def save_model(self, request, obj, form, change):
        """
        Change Method for save HourService data on Database
        """
        obj.user = request.user
        super().save_model(request, obj, form, change)
