# Generated by Django 4.2.8 on 2023-12-14 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathtrainer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='type',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='ProblemType',
        ),
    ]
