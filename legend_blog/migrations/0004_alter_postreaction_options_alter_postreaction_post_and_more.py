# Generated by Django 5.0.4 on 2024-04-15 05:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legend_blog', '0003_alter_postreaction_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postreaction',
            options={'verbose_name': 'Реакция на пост', 'verbose_name_plural': 'Реакции на посты'},
        ),
        migrations.AlterField(
            model_name='postreaction',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legend_blog.post', verbose_name='Пост'),
        ),
        migrations.AlterField(
            model_name='postreaction',
            name='reaction',
            field=models.CharField(choices=[('clown', 'Клоун'), ('like', 'Круть'), ('dislike', 'Ужас')], max_length=10, verbose_name='Тип реакции'),
        ),
        migrations.AlterField(
            model_name='postreaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterModelTable(
            name='postreaction',
            table='reaction',
        ),
    ]
