from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from evaluations.domain.user.entity import User
from evaluations.models.employee import DbEmployee


class UserManager(BaseUserManager["DbUser"]):
    def create_user(
        self,
        employee_code: str,
        employee: DbEmployee,
        password: str | None = None,
        name: str | None = None,
        **extra_fields: object,
    ) -> "DbUser":
        if not employee_code:
            raise ValueError("employee_code is required.")
        if employee is None:
            raise ValueError("employee is required.")
        if not name:
            name = employee.name
        if not name:
            raise ValueError("name is required.")
        employee_code = self.model.normalize_username(employee_code)
        user = self.model(
            employee_code=employee_code, employee=employee, name=name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        employee_code: str,
        employee: DbEmployee,
        password: str | None = None,
        name: str | None = None,
        **extra_fields: object,
    ) -> "DbUser":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(employee_code, employee, password, name, **extra_fields)


class DbUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    employee = models.OneToOneField(
        DbEmployee,
        on_delete=models.CASCADE,
        related_name="user",
    )
    employee_code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "employee_code"
    REQUIRED_FIELDS = ["employee", "name"]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.employee_code}{self.name}"

    def to_entity(self) -> User:
        return User(
            uuid=self.uuid,
            employee_uuid=self.employee_id,
            employee_code=self.employee_code,
            password=self.password,
            is_active=self.is_active,
            name=self.name,
        )
