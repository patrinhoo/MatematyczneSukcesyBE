from django.contrib import admin

from apps.users.models.user_orm import UserOrm


admin.site.register(UserOrm)
