from datetime import datetime
from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, DateTimeInput, NumberInput, CheckboxInput
from .models import Teachers, Training, Groups, Members, Schedule, Payment, Reviews, Claim, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

class TeachersForm(forms.ModelForm):
    class Meta:
        model = Teachers
        fields = ('surname', 'name', 'patronymic', 'details', 'photo')
        widgets = {
            'surname': TextInput(attrs={"size":"100"}),
            'name': TextInput(attrs={"size":"100"}),
            'patronymic': TextInput(attrs={"size":"100"}),   
            'details': Textarea(attrs={'cols': 100, 'rows': 3}),
        }
    # Метод-валидатор для поля surname
    def clean_surname(self):
        data = self.cleaned_data['surname']
        # Ошибка если начинается не с большой буквы
        if data.istitle() == False:
            raise forms.ValidationError(_('Value must start with a capital letter'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data 
    # Метод-валидатор для поля name
    def clean_name(self):
        data = self.cleaned_data['name']
        # Ошибка если начинается не с большой буквы
        if data.istitle() == False:
            raise forms.ValidationError(_('Value must start with a capital letter'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data 
    # Метод-валидатор для поля patronymic
    def clean_patronymic(self):
        data = self.cleaned_data['patronymic']
        # Ошибка если начинается не с большой буквы
        if data is not None:
            if data.istitle() == False:
                raise forms.ValidationError(_('Value must start with a capital letter'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ('title', 'details')
        widgets = {
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля title	
    def clean_title(self):
        data = self.cleaned_data['title']
        # Ошибка если такое значение уже есть в базе данных
        if Training.objects.filter(title=data).exists():
            raise forms.ValidationError("Value is already exists")
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data 

class GroupsForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ('training', 'title', 'details', 'teachers')
        widgets = {
            'training': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
            'teachers': forms.Select(attrs={'class': 'chosen'}),
        }
        labels = {
            'training': _('training'),            
            'teachers': _('teachers'),            
        }
    # Метод-валидатор для поля title	
    def clean_title(self):
        data = self.cleaned_data['title']
        # Ошибка если такое значение уже есть в базе данных
        if Groups.objects.filter(title=data).exists():
            raise forms.ValidationError("Value is already exists")
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data 

class MembersForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ('groups', 'user')
        widgets = {
            'groups': forms.Select(attrs={'class': 'chosen'}),
            'user': forms.Select(attrs={'class': 'chosen'}),
        }
        labels = {
            'groups': _('groups'),            
            'user': _('user'),            
        }
    # Валидатор нескольких полей
    def clean(self):
        cleaned_data = super().clean()
        _groups = cleaned_data.get("groups")
        _user = cleaned_data.get("user")
        # Один и тот же человек не может быть в одной группе
        if Members.objects.filter(groups=_groups).filter(user=_user).exists():
            raise forms.ValidationError("Value is already exists")

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('dates', 'groups')
        widgets = {
            'dates': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'groups': forms.Select(attrs={'class': 'chosen'}),            
        }
        labels = {
            'groups': _('groups'),            
        }
    # Метод-валидатор для поля dates
    def clean_dates(self):        
        if isinstance(self.cleaned_data['dates'], datetime) == True:
            data = self.cleaned_data['dates']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    
    # Валидатор нескольких полей
    def clean(self):
        cleaned_data = super().clean()
        _dates = cleaned_data.get("dates")
        _groups = cleaned_data.get("groups")
        # Один и тот же человек не может быть в одной группе
        if Schedule.objects.filter(groups=_groups).filter(dates=_dates).exists():
            raise forms.ValidationError("Value is already exists")

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('datep', 'amount', 'user')
        widgets = {
            'datep': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'amount': NumberInput(attrs={"size":"10"}),
            'user': forms.Select(attrs={'class': 'chosen'}),
        }
        labels = {
            'user': _('user'),            
        }
    # Метод-валидатор для поля datep
    def clean_datep(self):        
        if isinstance(self.cleaned_data['datep'], datetime) == True:
            data = self.cleaned_data['datep']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    
    # Метод-валидатор для поля amount
    def clean_amount(self):
        data = self.cleaned_data['amount']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Amount must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('details', 'rating')
        widgets = {
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
            'rating': forms.NumberInput(attrs={'max': '5', 'min': '1'}),            
        }

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ('training', 'details')
        widgets = {
            'training': forms.Select(attrs={'class': 'chosen'}),            
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
        labels = {
            'training': _('training'),            
        }

class ClaimFormEdit(forms.ModelForm):
    class Meta:
        model = Claim
        #fields = ('user', 'training', 'details', 'result')
        fields = ('result',)
        widgets = {
            #'user': forms.Select(attrs={'class': 'chosen', 'disabled': 'true'}),            
            #'training': forms.Select(attrs={'class': 'chosen', 'disabled': 'true'}),            
            #'details': Textarea(attrs={'cols': 100, 'rows': 10, 'readonly': 'readonly'}),           
            'result': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
        #labels = {
        #    'training': _('training'),            
        #}


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'dater': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')