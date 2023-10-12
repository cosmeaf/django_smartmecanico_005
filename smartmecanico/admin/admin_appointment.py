from django import forms
from django.contrib import admin
from employee_management.models import EmployeeInfo
from smartmecanico.models.appointment_model import Appointment

class AppointmentAdminForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=EmployeeInfo.objects.all(), required=False)

    class Meta:
        model = Appointment
        fields = "__all__"

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentAdminForm
    list_display = ('protocol', 'user', 'address', 'vehicle', 'service', 'hour', 'day', 'employee_name',)
    list_filter = ('service', 'employee', 'day')
    search_fields = ('protocol', 'user__username', 'address__id', 'vehicle__brand', 'vehicle__model', 'day')
    date_hierarchy = 'day'
    readonly_fields = ('protocol', 'created_at', 'updated_at', 'deleted_at')
    autocomplete_fields = ['user', 'address', 'vehicle', 'service', 'employee']

    fieldsets = (
        ('Informações do Agendamento', {
            'fields': ('user', 'address', 'vehicle', 'service', 'hour', 'day', 'protocol', 'employee'),
        }),
        ('Datas e Horários', {
            'fields': ('created_at', 'updated_at', 'deleted_at'),
            'classes': ('collapse',),
        })
    )

    def employee_name(self, obj):
        if obj.employee:
            return f"{obj.employee.first_name} {obj.employee.last_name}"
        return "-"
    employee_name.short_description = 'Mechanic assigned'

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except Exception as e:
            if not change:
                self.message_user(request, f"Erro ao criar o agendamento: {str(e)}", level='error')
            else:
                self.message_user(request, f"Erro ao atualizar o agendamento: {str(e)}", level='error')

    def assign_employee(self, request, queryset):
        employee_id = request.POST.get('employee_id')
        if employee_id:
            try:
                new_employee = EmployeeInfo.objects.get(id=employee_id)
                for appointment in queryset:
                    appointment.employee = new_employee
                    appointment.save()
                    print(appointment)
                self.message_user(request, f"Mecânico designado com sucesso.", level='success')
            except EmployeeInfo.DoesNotExist:
                self.message_user(request, f"Mecânico não encontrado.", level='error')
            except Exception as e:
                self.message_user(request, f"Erro ao designar o mecânico: {str(e)}", level='error')
        else:
            self.message_user(request, f"Selecione um mecânico.", level='error')

    assign_employee.short_description = "Atribuir funcionário selecionado"
    actions = [assign_employee]
