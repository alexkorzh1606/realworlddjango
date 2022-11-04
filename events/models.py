from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

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

    EVENT_OCCUPANCY_LHALF = '<= 50%'
    EVENT_OCCUPANCY_GHALF = '> 50%'
    EVENT_OCCUPANCY_SOLDOUT = 'sold-out'

    EVENT_OCCUPANCY_0_QUERY = '0'
    EVENT_OCCUPANCY_1_QUERY = '1'
    EVENT_OCCUPANCY_2_QUERY = '2'

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
    logo = models.ImageField(upload_to='events/events', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[str(self.pk)])

    @property
    def rate(self):
        event_reviews_list = self.reviews.all()
        rate_sum = 0
        for review in event_reviews_list:
            rate_sum += review.rate
        rate_result = round(rate_sum / event_reviews_list.count(), 1)
        return rate_result

    @property
    def logo_url(self):
        return self.logo.url if self.logo else f'{settings.STATIC_URL}images/svg-icon/event.svg'

    def display_enroll_count(self):
        return self.enrolls.count()
    display_enroll_count.short_description = 'Количество записей'

    def places_left(self):
        return self.participants_number - self.enrolls.count()
    places_left_prop = property(places_left)

    def occupancy_estimation(self):
        return self.places_left_prop / self.participants_number
    occupancy_estimation_prop = property(occupancy_estimation)

    def estimate_places_left(self):
        value = ''
        if self.occupancy_estimation_prop >= 0.5:
            value = self.EVENT_OCCUPANCY_0_QUERY
        elif self.occupancy_estimation_prop < 0.5 and self.places_left_prop != 0:
            value = self.EVENT_OCCUPANCY_1_QUERY
        elif self.places_left_prop == 0:
            value = self.EVENT_OCCUPANCY_2_QUERY
        return value
    estimate_places_left_prop = property(estimate_places_left)

    def display_places_left(self):
        occupancy = ''
        if self.estimate_places_left_prop == '1':
            occupancy = self.EVENT_OCCUPANCY_GHALF
        elif self.estimate_places_left_prop == '0':
            occupancy = self.EVENT_OCCUPANCY_LHALF
        elif self.estimate_places_left_prop == '2':
            occupancy = self.EVENT_OCCUPANCY_SOLDOUT
        return f'{self.places_left_prop} ({occupancy})'
    display_places_left.short_description = 'Осталось мест'


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
