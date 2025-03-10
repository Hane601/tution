# Generated by Django 5.1.4 on 2025-03-05 07:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=7, unique=True)),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=10)),
                ('Mahaoya', models.BooleanField(default=False)),
                ('Kakirihena', models.BooleanField(default=False)),
                ('Maths', models.BooleanField(default=False)),
                ('English', models.BooleanField(default=False)),
                ('Science', models.BooleanField(default=False)),
                ('Sinhala', models.BooleanField(default=False)),
                ('Buddhism', models.BooleanField(default=False)),
                ('History', models.BooleanField(default=False)),
                ('year', models.CharField(max_length=4)),
                ('qr', models.ImageField(blank=True, null=True, upload_to='qrcodes/')),
            ],
        ),
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dates', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('contact', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=128)),
                ('English', models.BooleanField(default=False)),
                ('Maths', models.BooleanField(default=False)),
                ('Science', models.BooleanField(default=False)),
                ('Sinhala', models.BooleanField(default=False)),
                ('Buddhism', models.BooleanField(default=False)),
                ('History', models.BooleanField(default=False)),
                ('Mahaoya', models.BooleanField(default=False)),
                ('Kakirihena', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=7, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('specific_class', models.CharField(max_length=200)),
                ('main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='Students.register')),
            ],
        ),
    ]
