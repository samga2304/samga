from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from django.core.files.storage import default_storage as storage  

from django.contrib.auth.models import User

import math

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Преподаватели
class Teachers(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE) 
    surname = models.CharField(_('surname'), max_length=64)
    name = models.CharField(_('name'), max_length=64)
    patronymic = models.CharField(_('patronymic'), max_length=64, blank=True, null=True)    
    details = models.TextField(_('details_teachers'))
    photo = models.ImageField(_('photo_teachers'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'teachers'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['surname']),
            models.Index(fields=['name']),
            models.Index(fields=['patronymic']),
        ]
        # Сортировка по умолчанию
        ordering = ['surname', 'name', 'patronymic']        
    def __str__(self):
        # Вывод в тег Select
        return "{} {} {}".format(self.surname, self.name, self.patronymic)
    @property
    def fio(self):
        # Возврат ФИО
        return '%s %s %s' % (self.surname, self.name, self.patronymic)
    @property
    def fio_shortcut(self):
        # Возврат Фамилия И.О.
        fio = self.surname + " "  + self.name[0] + "."
        if self.patronymic is not None:
            fio = fio + " " + self.patronymic[0] + "."
        return '%s' % (fio)

# Курс
class Training(models.Model):
    title = models.CharField(_('training_title'), unique=True, max_length=196)
    details = models.TextField(_('training_details'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'training'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод Название в тег SELECT 
        return self.title

# Группы
class Groups(models.Model):
    training = models.ForeignKey(Training, related_name='groups_training', on_delete=models.CASCADE)
    title = models.CharField(_('group_title'), unique=True, max_length=256)
    details = models.TextField(_('group_details'))
    teachers = models.ForeignKey(Teachers, related_name='groups_teachers', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'groups'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['training']),
        ]
    def __str__(self):
        # Вывод Название в тег SELECT 
        return self.title

# Состав группы
class Members(models.Model):
    groups = models.ForeignKey(Groups, related_name='members_groups', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='members_user', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'members'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['groups']),
            models.Index(fields=['user']),
        ]
        # unique_together - уникальный индекс по нескольким полям
        unique_together = (
           'groups',
           'user',
        )

# Расписание занятий
class Schedule(models.Model):
    dates = models.DateTimeField(_('dates'))
    groups = models.ForeignKey(Groups, related_name='schedule_groups', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'schedule'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dates']),
            models.Index(fields=['groups']),
        ]
        # Сортировка по умолчанию
        ordering = ['dates']
        # unique_together - уникальный индекс по нескольким полям
        unique_together = (
           'dates',
           'groups',
        )

# Оплата 
class Payment(models.Model):
    datep = models.DateTimeField(_('datep'))
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2)
    user = models.ForeignKey(User, related_name='payment_user', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'payment'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datep']),
        ]
        # Сортировка по умолчанию
        ordering = ['datep']

# Отзывы 
class Reviews(models.Model):
    dater = models.DateTimeField(_('dater_reviews'), auto_now_add=True)
    rating = models.IntegerField(_('rating'), blank=True, null=True)
    details = models.TextField(_('details_reviews'))
    user = models.ForeignKey(User, related_name='reviews_user', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'reviews'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dater']),
        ]
        # Сортировка по умолчанию
        ordering = ['dater']

# Заявки пользователей
class Claim(models.Model):
    dater = models.DateTimeField(_('dater_claim'), auto_now_add=True)
    user = models.ForeignKey(User, related_name='claim_user', on_delete=models.CASCADE)
    training = models.ForeignKey(Training, related_name='claim_training', on_delete=models.CASCADE)
    details = models.TextField(_('claim_details'))
    result = models.TextField(_('result'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'claim'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dater']),
        ]
        # Сортировка по умолчанию
        ordering = ['dater']
        
# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('title_news'), max_length=256)
    details = models.TextField(_('details_news'))
    photo = models.ImageField(_('photo_news'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
    #def save(self):
    #    super().save()
    #    img = Image.open(self.photo.path) # Open image
    #    # resize image
    #    if img.width > 512 or img.height > 700:
    #        proportion_w_h = img.width/img.height  # Отношение ширины к высоте 
    #        output_size = (512, int(512/proportion_w_h))
    #        img.thumbnail(output_size) # Изменение размера
    #        img.save(self.photo.path) # Сохранение

