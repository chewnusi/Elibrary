# Generated by Django 4.2.7 on 2023-12-01 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuedbook',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='issued_books', to='library.book'),
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='issued_books', to='library.person'),
        ),
    ]
