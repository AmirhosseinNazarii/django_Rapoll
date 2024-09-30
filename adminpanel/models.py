from django.db import models

class Block(models.Model):
    CITY_CHOICES = [
        ('تهران', 'تهران'),
    ]

    NEIGHBORHOOD_CHOICES = [
        ('زعفرانیه', 'زعفرانیه'),
        ('نیاوران', 'نیاوران'),
        ('قیطریه', 'قیطریه'),
        ('الهیه', 'الهیه'),
        ('فرمانیه', 'فرمانیه'),
        ('ولنجک', 'ولنجک'),
        ('نازی آباد', 'نازی آباد'),
        ('پاسداران', 'پاسداران'),
        ('سعادت آباد', 'سعادت آباد'),
        ('شهرک غرب', 'شهرک غرب'),
        ('پونک', 'پونک'),
        ('جردن (آفریقا)', 'جردن (آفریقا)'),
        ('میرداماد', 'میرداماد'),
        ('باغ فردوس', 'باغ فردوس'),
        ('ونک', 'ونک'),
        ('جوادیه', 'جوادیه'),
        ('آجودانیه', 'آجودانیه'),
        ('یوسف آباد', 'یوسف آباد'),
        ('تهرانپارس', 'تهرانپارس'),
    ]

    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    neighborhood = models.CharField(max_length=100, choices=NEIGHBORHOOD_CHOICES)
    street = models.CharField(max_length=100)
    alley = models.CharField(max_length=100)
    block_number = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)  # False برای "قابل فروش" و True برای "فروخته شده"

    def __str__(self):
        return f'{self.city} - {self.neighborhood} - {self.block_number}'
