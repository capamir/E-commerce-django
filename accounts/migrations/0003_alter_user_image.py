# Generated by Django 4.1.6 on 2023-03-02 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_image_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='accounts/images/default.jpg', null=True, upload_to='accounts/images/'),
        ),
    ]