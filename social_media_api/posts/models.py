from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='المؤلف'
    )
    title = models.CharField(max_length=255, verbose_name='العنوان')
    # تأكد من وجود هذا السطر
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
    # تأكد من وجود هذا السطر
    content = models.TextField(verbose_name='المحتوى') 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'تعليق'
        verbose_name_plural = 'تعليقات'

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:20]}...'