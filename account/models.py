from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from base.models import create_id
 
 
class UserManager(BaseUserManager):
 
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username = username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
 
 
class User(AbstractBaseUser):
    id = models.CharField(default=create_id, primary_key=True, max_length=32)
    username = models.CharField(
        max_length=50, blank=True, default='Anonymous')
    email = models.EmailField(max_length=255, unique=True)
    newsletter = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'username'
    REQUIRED_FIELDS = ['username',]
 
    def __str__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
 
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.USERNAME_FIELD
        except AttributeError:
            return "email"
        
    @classmethod
    def get_username_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "username"
 
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
 
 
class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    name = models.CharField(default='', blank=True, max_length=50)
    zipcode = models.CharField(default='', blank=True, max_length=8)
    prefecture = models.CharField(default='', blank=True, max_length=50)
    city = models.CharField(default='', blank=True, max_length=50)
    address1 = models.CharField(default='', blank=True, max_length=50)
    address2 = models.CharField(default='', blank=True, max_length=50)
    tel = models.CharField(default='', blank=True, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name
 
 
# OneToOneFieldを同時に作成
@receiver(post_save, sender=User)
def create_onetoone(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
