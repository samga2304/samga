from django.contrib import admin

from .models import Teachers, Training, Groups, Members, Schedule, Payment, Reviews, Claim, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Teachers)
admin.site.register(Training)
admin.site.register(Groups)
admin.site.register(Members)
admin.site.register(Schedule)
admin.site.register(Payment)
admin.site.register(Reviews)
admin.site.register(Claim)
admin.site.register(News)