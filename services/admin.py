from django.contrib import admin
from django.utils.html import format_html
from .models import Service, HourService


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'image_tag', 'user')
    ordering = ['created_at']
    search_fields = ['name']
    exclude = ['user', ]
    list_display_links = ('name',)
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']

    def description_short(self, obj):
        return str(obj.description)[:30]

    description_short.short_description = 'Description'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{0}", style="width: 40px;" />'.format(obj.image.url))
        return "-"

    image_tag.short_description = 'Image'

    def delete(self, request, obj):
        """
        Delete Image From Media
        """
        if obj.image:
            storage, path = obj.image.storage, obj.image.path
            obj.image.delete()
        super(ServiceAdmin, self).delete(request, obj)

    def get_queryset(self, request):
        """
        Show result user by id
        """
        queryset = super(ServiceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user_id=request.user.id)

    def save_model(self, request, obj, form, change):
        """
        Change Method for save Service data on Database
        """
        obj.user = request.user
        super().save_model(request, obj, form, change)


class HourServiceAdmin(admin.ModelAdmin):
    list_display = ('hour', 'user')
    ordering = ['created_at']
    search_fields = ['hour', 'user__username']
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

    def save_model(self, request, obj, form, change):
        """
        Change Method for save HourService data on Database
        """
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(HourService, HourServiceAdmin)
admin.site.register(Service, ServiceAdmin)
