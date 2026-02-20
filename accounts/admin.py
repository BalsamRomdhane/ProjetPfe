from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
	model = User
	list_display = ('username', 'email', 'role', 'department', 'is_staff', 'is_active')
	fieldsets = UserAdmin.fieldsets + (
		(None, {'fields': ('role', 'department', 'keycloak_id')}),
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		(None, {'fields': ('role', 'department', 'keycloak_id')}),
	)
