# Generated by Django 5.1.1 on 2025-01-25 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspectionApp', '0009_inspection_question_3_inspection_question_4_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='question_7',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='What strategies are in place to ensure student engagement and learning outcomes?'),
        ),
    ]
