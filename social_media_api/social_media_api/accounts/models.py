from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # الحقول الإضافية
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # حقل المتابعين (Many-to-Many حقل يرجع لنفس النموذج)
    # symmetrical=False: لأن المتابعة ليست بالضرورة متبادلة (إذا تابعتني، لا يعني أنني تابعتك تلقائياً)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following', # الاسم العكسي (من يتابعني)
        blank=True
    )

    def __str__(self):
        return self.username