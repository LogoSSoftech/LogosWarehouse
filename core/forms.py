from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.models import User, CoreCompanies


class UserForm(UserCreationForm):

    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'user_image',
            'is_staff',
            'is_active',
            'password1',
            'password2',
            ]

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class RestorePasswordForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))


class CoreCompanyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off '
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = CoreCompanies

        fields = [
            'name',
            'rif_type',
            'rif',
            'company_image',
            'society',
            'email',
            'web_site',
            'phone1',
            'phone2',
            'address',
            'description',
            ]
