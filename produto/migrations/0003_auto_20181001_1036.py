# Generated by Django 2.0.2 on 2018-10-01 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_produto_preco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='slug',
            field=models.SlugField(max_length=120, null=True),
        ),
    ]