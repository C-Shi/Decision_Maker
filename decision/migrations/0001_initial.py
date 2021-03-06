# Generated by Django 2.1.3 on 2018-12-07 02:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('context', models.CharField(max_length=50)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creator', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('expire_on', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('activity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decision.Activity')),
            ],
        ),
    ]
