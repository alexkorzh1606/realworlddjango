from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=90, verbose_name='Категория', default='')

    def display_event_count(self):
        return self.events.count()
    display_event_count.short_description = 'Количество событий для категории'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Feature(models.Model):
    title = models.CharField(max_length=90, verbose_name='Свойство события', default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Свойства событий'
        verbose_name = 'Свойство события'


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название', default='')
    description = models.TextField(verbose_name='Описание', default='')
    date_start = models.DateTimeField(verbose_name='Дата начала')
    participants_number = models.PositiveSmallIntegerField(
        verbose_name='Количество участников',
        validators=[MinValueValidator(0), (MaxValueValidator(10000))]
    )
    is_private = models.BooleanField(verbose_name='Частное', default=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_DEFAULT, default='', related_name='events', verbose_name='Категория')
    features = models.ManyToManyField(Feature, verbose_name='Свойства события')

    def __str__(self):
        return self.title

    def display_enroll_count(self):
        return self.enrolls.count()
    display_enroll_count.short_description = 'Количество записей'
    show_enroll_count = property(display_enroll_count)

    def places_left(self):
        return self.participants_number - self.enrolls.count()
    places_left_prop = property(places_left)

    def occupancy_estimation(self):
        return self.places_left_prop / self.participants_number
    occupancy_estimation_prop = property(occupancy_estimation)

    def display_places_left(self):
        occupancy = ''
        if self.occupancy_estimation_prop > 0.5:
            occupancy = '> 50%'
        elif self.occupancy_estimation_prop <= 0.5 and self.places_left_prop != 0:
            occupancy = '<= 50%'
        elif self.places_left_prop == 0:
            occupancy = 'sold-out'
        return f'{self.places_left_prop} ({occupancy})'
    display_places_left.short_description = 'Осталось мест'
    show_places_left = property(display_places_left)

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'


class Enroll(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_DEFAULT, default='', related_name='enrolls', verbose_name='Пользователь')
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_DEFAULT, default='', related_name='enrolls', verbose_name='Событие')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name_plural = 'Записи на события'
        verbose_name = 'Запись на событие'


class Review(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_DEFAULT, default='', related_name='reviews', verbose_name='Пользователь')
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_DEFAULT, default='', related_name='reviews', verbose_name='Событие')
    rate = models.PositiveSmallIntegerField(null=True, default='', verbose_name='Оценка пользователя')
    text = models.TextField(null=True, default='', blank=True, verbose_name='Текст отзыва')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'

    def __str__(self):
        return f'{self.user} - {self.rate} - {self.event}'
