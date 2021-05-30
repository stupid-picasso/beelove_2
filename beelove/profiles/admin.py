from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from profiles.models import users



class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username',)
	# readonly_fields=('userid', 'date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(users, AccountAdmin)