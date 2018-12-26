from django import forms
from skaba.models import Guild, UserProfile, Event
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'slug', 'eventdate', 'points', 'guild', 'repeats']

    name = forms.CharField(label='Event name', max_length=128, min_length=1)
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={
        'rows': 2,
        'cols': 19
        }))
    guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
    eventdate = forms.DateField(widget=forms.SelectDateWidget(years={2018, 2019}))
    repeats = forms.IntegerField(label='Repeats', initial=1, min_value=0)
    points = forms.IntegerField(label='Points', min_value=0)

class AddUserForm(UserCreationForm):
    #role choices
    role_choices = (('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin'))
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    #role = forms.CharField(label='User\'s role', required=False, initial='user')
    role = forms.ChoiceField(choices=role_choices)
    guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
    is_kv = forms.BooleanField(required=False)
    is_tf = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_kv', 'is_tf', 'role')

    def save(self,commit = True):
        user = super(AddUserForm, self).save(commit = True)
        user_profile = user.profile
        user_profile.role = self.cleaned_data['role']
        user_profile.guild = self.cleaned_data['guild']
        user_profile.is_kv = self.cleaned_data['is_kv']
        user_profile.is_tf = self.cleaned_data['is_tf']
        user_profile.save()
        return user, user_profile

        if commit:
            user.save()
            return user

class EditUserForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)
    class Meta:
        model = User
        fields = ('email', )

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        new_password = self.cleaned_data['password1']
        if (user.check_password(self.cleaned_data['old_password']) and 
                new_password == self.cleaned_data['password2'] and
                len(new_password) > 5):
            user.set_password(new_password)

        if commit:
            user.save()

        return user

class ImportUserForm(forms.Form):
    guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
    csv_file = forms.FileField(label='CSV file',
        help_text='Order is First name, Last name, e-mail, is_KV, is_TF, Password')

class ImportEventForm(forms.Form):
    guild = forms.ModelChoiceField(queryset=Guild.objects.all(), empty_label=None)
    csv_file = forms.FileField(label='CSV file',
        help_text='Order is Event name, desc(fi), desc(en), desc(swe), Points, url, repeats, date')

# Admins/moderators can modify all user info
# Optimally the admin edit form would just be one form,
# But I had trouble with that
class AdminEditProfileForm(forms.ModelForm):
    role_choices = (('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin'))
    role = forms.ChoiceField(choices=role_choices)

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def save(self, commit = True):
        profile = super(AdminEditProfileForm, self).save(commit = True)
        profile.role = self.cleaned_data['role']
        profile.guild = self.cleaned_data['guild']
        profile.is_kv = self.cleaned_data['is_kv']
        profile.is_tf = self.cleaned_data['is_tf']
        return profile

        if commit:
            profile.save()

        return profile

class AdminEditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(AdminEditUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
