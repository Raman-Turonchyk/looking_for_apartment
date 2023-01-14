from django.db import models


class City(models.Model):
    city = models.CharField(max_length=30,
                            help_text='Введите название города',
                            verbose_name='Город')

    def __str__(self):
        return self.city


class Link(models.Model):
    link = models.CharField(max_length=150, help_text='Ссылка на квартиру')
    city = models.ForeignKey('City', on_delete=models.CASCADE, help_text='Выберите город',
                             verbose_name='Город')

    def __str__(self):
        return self.link
