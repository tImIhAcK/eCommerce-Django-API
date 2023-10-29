from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError



# Create your models here
class MyUserManager(UserManager):
    def _create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
        
class User(AbstractUser, PermissionsMixin):
    username=None
    
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
        help_text=_('Required'))

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        ordering = ['email',]
        
        
def validate_image_type(value):
    if not value.name.endswith('.jpg') and not value.name.endswith('.jpeg') and not value.name.endswith('.png'):
        raise ValidationError(_('Invalid image type. Only JPG, JPEG, and PNG formats are allowed.'))

def validate_image_size(value):
    # Set the maximum file size in bytes (e.g., 5MB)
    max_size = 10 * 1024 * 1024  # 5MB

    if value.size > max_size:
        raise models.ValidationError("The file size exceeds the maximum allowed size.")


class Profile(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    gender = models.CharField(choices=GENDER, max_length=10, blank=True,null=True)
    phone = PhoneNumberField(blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='profile_pics/', blank=True,
                              validators=[validate_image_type, validate_image_size]
                              )
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return f'{self.full_name}'
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        