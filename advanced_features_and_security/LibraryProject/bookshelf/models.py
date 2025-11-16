from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

# ----------------------------------------------------
# 1. Custom User Manager
# ----------------------------------------------------

class CustomUserManager(BaseUserManager):
    """
    مدير مخصص لنموذج CustomUser.
    يسمح بإنشاء المستخدمين العاديين والمشرفين (Superusers) باستخدام البريد الإلكتروني.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# ----------------------------------------------------
# 2. Custom User Model (نموذج المستخدم المخصص)
# ----------------------------------------------------

class CustomUser(AbstractUser):
    """
    نموذج مستخدم مخصص يضيف حقول 'date_of_birth' و 'profile_photo'.
    """
    # نستخدم البريد الإلكتروني كاسم مستخدم فريد بدلاً من حقل username الافتراضي
    email = models.EmailField(unique=True, null=True, blank=True)
    
    # الحقول الإضافية المطلوبة
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/', 
        null=True, 
        blank=True,
        # يمكن إضافة مدقق لضمان امتدادات الصور
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    
    # تحديد الحقل الذي سيستخدم لتسجيل الدخول
    USERNAME_FIELD = 'email'
    # إزالة email من قائمة الحقول المطلوبة عند إنشاء المستخدم
    REQUIRED_FIELDS = ['username'] 

    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.username

# ----------------------------------------------------
# 3. User Profile Model (نموذج ملف التعريف الإضافي)
# ----------------------------------------------------

class UserProfile(models.Model):
    """
    نموذج لملف تعريف المستخدم يحمل المعلومات الإضافية، ومرتبط بـ CustomUser.
    """
    # الرابط الرئيسي للمستخدم
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    # حقل لتخزين دور المستخدم (عضو، أمين مكتبة، أو مشرف)
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('librarian', 'Librarian'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    
    # يمكنك إضافة حقول أخرى هنا مثل العنوان، رقم الهاتف، إلخ.

    def __str__(self):
        return f"{self.user.email}'s Profile"

# ----------------------------------------------------
# 4. Signals (الإشارات لإنشاء ملف التعريف تلقائياً)
# ----------------------------------------------------

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """إنشاء ملف تعريف للمستخدم فور إنشائه."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """حفظ ملف تعريف المستخدم بعد تحديث المستخدم."""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # هذه الحالة تحدث إذا كان الحساب قديمًا ولم يكن لديه ملف تعريف
        UserProfile.objects.create(user=instance)

# ----------------------------------------------------
# 5. نماذج الكتب والمكتبات (إذا كانت مطلوبة هنا)
# ----------------------------------------------------
# **ملاحظة:** إذا كانت هذه النماذج مطلوبة في تطبيق 'bookshelf'، يجب إضافتها هنا.
# إذا كانت مخصصة لتطبيق 'relationship_app'، فيجب أن تبقى هناك.

# # مثال (يجب إضافته فقط إذا كان نظام التحقق يتوقعه هنا):
# class Book(models.Model):
#     title = models.CharField(max_length=200)
#     # ... يرجى إضافة باقي النماذج التي تتوقعها المهمة في هذا التطبيق