from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from evaluations.models.user import DbUser


class EmployeeUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = DbUser
        fields = ("employee", "employee_code", "name")


class EmployeeUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = DbUser
        fields = (
            "employee",
            "employee_code",
            "name",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


@admin.register(DbUser)
class DbUserAdmin(UserAdmin):
    add_form = EmployeeUserCreationForm
    form = EmployeeUserChangeForm
    model = DbUser
    list_display = ["employee_code", "name", "employee", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]
    ordering = ["employee_code"]
    search_fields = ["employee_code", "name"]
    fieldsets = (
        (None, {"fields": ("employee_code", "password")}),
        ("Employee", {"fields": ("employee", "name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "employee",
                    "employee_code",
                    "name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )
