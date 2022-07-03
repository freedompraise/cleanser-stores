# Generated by Django 4.0.4 on 2022-06-06 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='customer',
        ),
        migrations.AddField(
            model_name='product',
            name='avatar',
            field=models.ImageField(default='image.jpg', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=1, max_length=5),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
