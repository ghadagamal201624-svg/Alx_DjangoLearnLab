# relationship_app/models.py

from django.db import models
# نستورد AbstractUser و BaseUserManager بدلاً من User الافتراضي
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import datetime
import os
from django.conf import settings # لاستخدام AUTH_USER_MODEL لاحقاً


# --- 1. Custom User Manager (الخطوة 3) ---
class CustomUserManager(BaseUserManager):
    """مدير المستخدم المخصص الذي يتعامل مع CustomUser."""

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username must be set'))
        email = self.normalize_email(email)
        
        # تعيين قيمة افتراضية لحقل date_of_birth
        extra_fields.setdefault('date_of_birth', datetime.date(2000, 1, 1)) 
        
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
            
        extra_fields.setdefault('date_of_birth', datetime.date(1990, 1, 1)) 
        
        return self.create_user(username, email, password, **extra_fields)


# --- 2. Custom User Model (الخطوة 1) ---
class CustomUser(AbstractUser):
    # حقول إضافية مطلوبة
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='users_photos/', null=True, blank=True)

    # استخدام المدير المخصص
    objects = CustomUserManager()

    def __str__(self):
        return self.username
# ----------------------------------------------------------------------

# تعريف خيارات الأدوار (يبقى كما هو)
ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
)

# ----------------------------------------------------------------------
# 3. تحديث مراجع المستخدم (الخطوة 5: UserProfile يستخدم CustomUser)
# ----------------------------------------------------------------------

class UserProfile(models.Model):
    # استخدام settings.AUTH_USER_MODEL لربط النموذج المخصص
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        # نستخدم instance.user.username للوصول إلى حقول CustomUser
        return f"{self.user.username}'s Profile ({self.role})"


# 4. تحديث الإشارات (Signals) لاستخدام CustomUser
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """ينشئ ملف تعريف المستخدم تلقائيًا عند إنشاء مستخدم جديد."""
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """يحفظ ملف تعريف المستخدم عند حفظ المستخدم."""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save() 
# ----------------------------------------------------------------------

# النماذج الأخرى تبقى كما هي، لكن يجب التأكد من ترتيبها

class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField(default=2000)
    class Meta:
        permissions = [
            ("can_add_book", "Can add new book entries"),
            ("can_change_book", "Can edit existing book entries"),
            ("can_delete_book", "Can delete book entries"),
        ]
    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"Librarian: {self.name} for {self.library.name}"