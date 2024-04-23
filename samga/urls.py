"""samga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static

from academy import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('i18n/', include('django.conf.urls.i18n')),

    path('export/excel/', views.export_excel, name='export_excel'),     
    path('cabinet/', views.cabinet, name='cabinet'),

    path('teachers/index/', views.teachers_index, name='teachers_index'),
    path('teachers/list/', views.teachers_list, name='teachers_list'),
    path('teachers/create/', views.teachers_create, name='teachers_create'),
    path('teachers/edit/<int:id>/', views.teachers_edit, name='teachers_edit'),
    path('teachers/delete/<int:id>/', views.teachers_delete, name='teachers_delete'),
    path('teachers/read/<int:id>/', views.teachers_read, name='teachers_read'),

    path('training/index/', views.training_index, name='training_index'),
    path('training/create/', views.training_create, name='training_create'),
    path('training/edit/<int:id>/', views.training_edit, name='training_edit'),
    path('training/delete/<int:id>/', views.training_delete, name='training_delete'),
    path('training/read/<int:id>/', views.training_read, name='training_read'),

    path('groups/index/', views.groups_index, name='groups_index'),
    path('groups/create/', views.groups_create, name='groups_create'),
    path('groups/edit/<int:id>/', views.groups_edit, name='groups_edit'),
    path('groups/delete/<int:id>/', views.groups_delete, name='groups_delete'),
    path('groups/read/<int:id>/', views.groups_read, name='groups_read'),

    path('members/index/', views.members_index, name='members_index'),
    path('members/create/', views.members_create, name='members_create'),
    path('members/edit/<int:id>/', views.members_edit, name='members_edit'),
    path('members/delete/<int:id>/', views.members_delete, name='members_delete'),
    path('members/read/<int:id>/', views.members_read, name='members_read'),

    path('schedule/index/', views.schedule_index, name='schedule_index'),
    path('schedule/list/', views.schedule_list, name='schedule_list'),
    path('schedule/create/', views.schedule_create, name='schedule_create'),
    path('schedule/edit/<int:id>/', views.schedule_edit, name='schedule_edit'),
    path('schedule/delete/<int:id>/', views.schedule_delete, name='schedule_delete'),
    path('schedule/read/<int:id>/', views.schedule_read, name='schedule_read'),

    path('payment/index/', views.payment_index, name='payment_index'),
    path('payment/create/', views.payment_create, name='payment_create'),
    path('payment/edit/<int:id>/', views.payment_edit, name='payment_edit'),
    path('payment/delete/<int:id>/', views.payment_delete, name='payment_delete'),
    path('payment/read/<int:id>/', views.payment_read, name='payment_read'),

    path('reviews/index/', views.reviews_index, name='reviews_index'),
    path('reviews/list/', views.reviews_list, name='reviews_list'),
    path('reviews/create/', views.reviews_create, name='reviews_create'),
    path('reviews/delete/<int:id>/', views.reviews_delete, name='reviews_delete'),
    
    path('claim/index/', views.claim_index, name='claim_index'),
    path('claim/create/', views.claim_create, name='claim_create'),
    path('claim/edit/<int:id>/', views.claim_edit, name='claim_edit'),
    path('claim/delete/<int:id>/', views.claim_delete, name='claim_delete'),
    path('claim/read/<int:id>/', views.claim_read, name='claim_read'),

    path('news/index/', views.news_index, name='news_index'),
    path('news/list/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/edit/<int:id>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:id>/', views.news_delete, name='news_delete'),
    path('news/read/<int:id>/', views.news_read, name='news_read'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logoutUser, name="logout"),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
