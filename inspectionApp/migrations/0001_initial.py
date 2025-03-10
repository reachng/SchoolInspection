# Generated by Django 5.1.1 on 2025-01-12 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=255)),
                ('sf_code', models.CharField(max_length=100, unique=True)),
                ('inspector_name', models.CharField(max_length=255)),
                ('inspection_date', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('question_1', models.TextField(blank=True, null=True)),
                ('question_2', models.CharField(blank=True, max_length=255, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='inspection_photos/')),
            ],
        ),
    ]
