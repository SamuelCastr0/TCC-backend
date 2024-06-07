from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

User = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'name', 'password1', 'password2')

class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'lattes', 'googleScholar', 'researchGate', 'orcid', 'github', 'course', 'category', 'oia')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'lattes', 'googleScholar', 'researchGate', 'orcid', 'github', 'course', 'category', 'oia'),
        }),
    )
    list_display = ('email', 'name', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    def save_model(self, request, obj, form, change):
        if change and 'password' in form.changed_data and form.cleaned_data['password']:
            new_password = form.cleaned_data['password']
            obj.set_password(new_password)
        elif not change and form.cleaned_data.get('password1') and form.cleaned_data['password1'] == form.cleaned_data['password2']:
            obj.set_password(form.cleaned_data['password1'])
        obj.save()

admin.site.register(User, UserAdmin)