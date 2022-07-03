# Generated by Django 3.0 on 2022-06-20 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20220610_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='colour',
            field=models.CharField(default='N/A', max_length=15),
        ),
        migrations.AlterField(
            model_name='product',
            name='avatar',
            field=models.ImageField(default='cart.jpg', null=True, upload_to=''),
        ),
    ]
