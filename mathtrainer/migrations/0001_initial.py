# Generated by Django 4.2.8 on 2023-12-14 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemType',
            fields=[
                ('type', models.TextField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('title', models.TextField(primary_key=True, serialize=False)),
                ('id', models.IntegerField()),
                ('problem', models.TextField()),
                ('level', models.TextField()),
                ('solution', models.TextField()),
                ('answer', models.TextField()),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathtrainer.problemtype')),
            ],
        ),
    ]
