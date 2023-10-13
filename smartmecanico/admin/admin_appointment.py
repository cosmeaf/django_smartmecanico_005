from django import forms
from django.contrib.admin.actions import delete_selected
from django.shortcuts import render
from django.contrib import admin
from employee_management.models import EmployeeInfo
from smartmecanico.models.appointment_model import Appointment
from smart_history.models import AppointmentHistory

class DeletionReasonForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, label="Justificativa", required=True)

class AppointmentAdminForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=EmployeeInfo.objects.all(), required=False)

    class Meta:
        model = Appointment
        fields = "__all__"

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentAdminForm
    list_display = ('protocol', 'user', 'address', 'vehicle', 'service', 'hour', 'day', 'employee_name')
    list_filter = ('service', 'employee', 'day')
    search_fields = ('protocol', 'user__email', 'address__id', 'vehicle__brand', 'vehicle__model', 'day')
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
            super().save_model(request, obj, form, change)
            if change:
                self.message_user(request, f"Agendamento atualizado com sucesso!", level='success')
            else:
                self.message_user(request, f"Agendamento criado com sucesso!", level='success')
        except Exception as e:
            if change:
                self.message_user(request, f"Erro ao atualizar o agendamento: {str(e)}", level='error')
            else:
                self.message_user(request, f"Erro ao criar o agendamento: {str(e)}", level='error')

    def assign_employee(self, request, queryset):
        employee_id = request.POST.get('employee_id')
        if employee_id:
            try:
                new_employee = EmployeeInfo.objects.get(id=employee_id)
                for appointment in queryset:
                    appointment.employee = new_employee
                    appointment.save()
                self.message_user(request, f"Mecânico designado com sucesso.", level='success')
            except EmployeeInfo.DoesNotExist:
                self.message_user(request, f"Mecânico não encontrado.", level='error')
            except Exception as e:
                self.message_user(request, f"Erro ao designar o mecânico: {str(e)}", level='error')
        else:
            self.message_user(request, f"Selecione um mecânico.", level='error')

    assign_employee.short_description = "Atribuir funcionário selecionado"

    def delete_selected_with_reason(self, request, queryset):
        if request.POST.get('post'):
            form = DeletionReasonForm(request.POST)
            if form.is_valid():
                for obj in queryset:
                    AppointmentHistory.objects.create(appointment=obj, event_type="delete", reason=form.cleaned_data['reason'])
                return delete_selected(self, request, queryset)
        else:
            form = DeletionReasonForm()

        return render(request, 'admin/delete_selected_with_reason.html', {
            'queryset': queryset,
            'form': form,
            'modeladmin': self
        })

    delete_selected_with_reason.short_description = "Deletar selecionados e fornecer justificativa"

    actions = [assign_employee, delete_selected_with_reason]
