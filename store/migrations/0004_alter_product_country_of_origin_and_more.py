# Generated by Django 4.0.4 on 2022-06-06 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_product_size_alter_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='country_of_origin',
            field=models.CharField(default='Nigeria', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.IntegerField(default=5),
        ),
    ]
