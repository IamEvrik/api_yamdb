# Generated by Django 3.2 on 2023-04-04 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_rename_genretitle_titlegenre'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_author_review',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('user', 'user'), ('moderator', 'moderator')], default='user', max_length=9, verbose_name='role'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='uq_author_review'),
        ),
    ]