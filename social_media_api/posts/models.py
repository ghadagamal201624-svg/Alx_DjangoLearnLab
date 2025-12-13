from django.db import models
from django.contrib.auth import get_user_model

# الحصول على نموذج المستخدم النشط المحدد في settings.AUTH_USER_MODEL
User = get_user_model()

class Post(models.Model):
    """
    نموذج لـ Post (منشور) في منصة التواصل الاجتماعي.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='المؤلف'
    )
    title = models.CharField(max_length=255, verbose_name='العنوان')
    content = models.TextField(verbose_name='المحتوى')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'منشور'
        verbose_name_plural = 'منشورات'

    def __str__(self):
        return f'{self.title} by {self.author.username}'


class Comment(models.Model):
    """
    نموذج لـ Comment (تعليق) على Post معين.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='المنشور'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='المؤلف'
    )
    content = models.TextField(verbose_name='المحتوى')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'تعليق'
        verbose_name_plural = 'تعليقات'

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:20]}...'