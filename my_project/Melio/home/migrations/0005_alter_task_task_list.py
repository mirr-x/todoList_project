# Generated by Django 5.0.6 on 2024-05-09 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_task_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasklist', to='home.tasklist'),
        ),
    ]
