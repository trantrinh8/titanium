# -*- coding: utf-8 -*-
from django import forms
from titanium.models import *
from django.contrib.auth.models import User
#form đăng nhập
class ContactForm(forms.Form):
        email   = forms.EmailField()
        password   = forms.CharField(widget = forms.PasswordInput)
        def clean(self):
            cleaned_data = super(ContactForm,self).clean()
            email = cleaned_data.get('email')
            password = cleaned_data.get('password')
            users = User.objects.all()
            if email is None:
                self._errors['email']=self.error_class(['Mời nhập email'])
            if password is None:
                self._errors['password'] = self.error_class(['Mời nhập password'])
            else:
                for user in users:
                    if user.email == email:
                        return cleaned_data
            raise forms.ValidationError("username hoặc password không tồn tại hoắc không đúng. Vui lòng kiểm tra lại.")
        
