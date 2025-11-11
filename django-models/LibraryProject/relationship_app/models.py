# relationship_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
# تعريف خيارات الأدوار
ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Librarian', 'Librarian'),
    ('Member', 'Member'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # الدور الافتراضي سيكون 'Member'
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.role})"

# ب. إعداد الإشارات (Signals) لإنشاء UserProfile تلقائيًا
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ينشئ ملف تعريف المستخدم تلقائيًا عند إنشاء مستخدم جديد."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """يحفظ ملف تعريف المستخدم عند حفظ المستخدم."""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()    

# 1. تعريف Book مرة واحدة فقط، ويجب أن يسبق Library
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField(default=2000) # تأكدي من وجود هذا الحقل هنا فقط
    class Meta:
        # ترتيب الأذونات: (اسم الكود, الاسم الواضح)
        permissions = [
            ("can_add_book", "Can add new book entries"),
            ("can_change_book", "Can edit existing book entries"),
            ("can_delete_book", "Can delete book entries"),
        ]
    def __str__(self):
        return self.title

# 2. تعريف Library (الذي يشير إلى Book)
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    def __str__(self):
        return self.name

# 3. تعريف Librarian
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"Librarian: {self.name} for {self.library.name}"