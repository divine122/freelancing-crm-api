from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Records

User = get_user_model()
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=240,  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=240,  widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].label = ''
        self.fields['first_name'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), label="")
    last_name =  forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), label="")
    email =  forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), label="")
    phone =  forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), label="")
    address =  forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}), label="")
    city =  forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), label="")
    state =  forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), label="")
    zipcode =  forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), label="")

    class Meta:
        model = Records
        exclude = ("user",)
