from django.db import models


# Create your models here.
class City(models.Model):
    city = models.CharField(max_length=30,
                            help_text='Введите название города',
                            verbose_name='Город')

    def __str__(self):
        return self.city


class Link(models.Model):
    link = models.CharField(max_length=150, help_text='Ссылка на квартиру', null=False)
    room = models.IntegerField(help_text='Количество комнат', null=True, blank=True)
    region = models.CharField(max_length=100, help_text='Район', null=True, blank=True)
    address = models.CharField(max_length=150, help_text='Адресс', null=True, blank=True)
    price = models.IntegerField(help_text='Цена', null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, help_text='Выберите город',
                             verbose_name='Город')

    def __str__(self):
        return f'{self.link}, {self.id}'
