# Generated by Django 2.1.1 on 2018-09-27 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200)),
            ],
            options={
                'db_table': 'categoria',
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120)),
                ('slug', models.SlugField(max_length=120)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='produto.Categoria')),
            ],
            options={
                'db_table': 'produto',
                'ordering': ('nome',),
            },
        ),
    ]
