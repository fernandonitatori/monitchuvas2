# Generated by Django 3.2.8 on 2021-10-27 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20211026_2043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sede',
            old_name='locacao_acao',
            new_name='locacao',
        ),
    ]
