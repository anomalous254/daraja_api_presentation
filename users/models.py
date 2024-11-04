from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings


class MyUserManager(BaseUserManager):
    def create_user(self, email,password=None, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None, **Kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **Kwargs
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", 'first_name']

    def __str__(self):
        return self.email



class MPesaTransaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mpesa_transactions"
    )
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Pending")  # e.g., Pending, Success, Failed
    transaction_date = models.DateTimeField(null=True, blank=True)
    mpesa_receipt_number = models.CharField(max_length=255,null=True, blank=True, unique=True )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.phone_number} - {self.amount} KES"

  
