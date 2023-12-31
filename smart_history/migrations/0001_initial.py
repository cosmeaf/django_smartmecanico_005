# Generated by Django 4.2.6 on 2023-10-12 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('smartmecanico', '0003_appointment_cancellation_reason'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('image_path', models.TextField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, max_length=500, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('is_active', models.BooleanField()),
                ('is_staff', models.BooleanField()),
                ('failed_login_attempts', models.PositiveIntegerField()),
                ('last_failed_login', models.DateTimeField(blank=True, null=True)),
                ('history_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Histórico de Usuário',
                'verbose_name_plural': 'Históricos de Usuários',
                'ordering': ['-user'],
            },
        ),
        migrations.CreateModel(
            name='ServiceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartmecanico.service')),
            ],
            options={
                'verbose_name': 'Histórico de Serviço',
                'verbose_name_plural': 'Históricos de Serviços',
                'ordering': ['-service'],
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event_type', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=10)),
                ('data_snapshot', models.JSONField(help_text="Snapshot of the object's data at this point in time")),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Histórico',
                'verbose_name_plural': 'Históricos',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='AppointmentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartmecanico.appointment')),
            ],
            options={
                'verbose_name': 'Histórico de Agendamento',
                'verbose_name_plural': 'Históricos de Agendamentos',
                'ordering': ['-appointment'],
            },
        ),
        migrations.CreateModel(
            name='AppointmentCancellationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancellation_reason', models.TextField(help_text='Justificativa para o cancelamento')),
                ('cancellation_date', models.DateTimeField(auto_now_add=True)),
                ('data_snapshot', models.JSONField(help_text="Snapshot of the appointment's data at the time of cancellation")),
                ('appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancellation_history', to='smartmecanico.appointment')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartmecanico.service')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelled_appointments', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartmecanico.vehicle')),
            ],
            options={
                'verbose_name': 'Histórico de Cancelamento de Agendamento',
                'verbose_name_plural': 'Históricos de Cancelamentos de Agendamentos',
                'ordering': ['-cancellation_date'],
            },
        ),
    ]
