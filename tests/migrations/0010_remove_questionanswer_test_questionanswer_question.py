# Generated by Django 5.2.4 on 2025-07-17 06:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0009_cefr_question_questionanswer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionanswer',
            name='test',
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tests.question'),
            preserve_default=False,
        ),
    ]
