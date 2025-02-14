# Generated by Django 5.1.6 on 2025-02-14 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_otp_expires_at_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('phone_number', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(default='Employee', max_length=50)),
            ],
        ),
    ]
