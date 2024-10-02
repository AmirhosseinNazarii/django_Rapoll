# Generated by Django 3.2 on 2024-10-02 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('neighborhood', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('alley', models.CharField(max_length=100)),
                ('block_number', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
