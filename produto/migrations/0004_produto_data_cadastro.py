# Generated by Django 2.1.1 on 2018-10-08 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_auto_20181001_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='data_cadastro',
            field=models.DateField(null=True),
        ),
    ]
