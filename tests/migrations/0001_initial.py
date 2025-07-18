# Generated by Django 5.2.4 on 2025-07-13 14:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Dtm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('started', models.DateTimeField()),
                ('ended', models.DateTimeField()),
                ('participants', models.ManyToManyField(related_name='dtm_participants', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dtm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.dtm')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=10000)),
                ('type', models.CharField(choices=[('single', 'Bitta javob tanlanadigan'), ('multiple', "Ko'p javob tanlanadigan"), ('matchable', 'Moslashtiriladigan'), ('writable', 'Javob yoziladigan')], max_length=10)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.block')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_1', models.TextField()),
                ('value_2', models.TextField(blank=True, null=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.test')),
            ],
        ),
    ]
