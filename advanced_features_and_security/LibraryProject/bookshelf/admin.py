from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile 

# --- 1. Custom Admin Model لـ CustomUser ---
class CustomUserAdmin(UserAdmin):
    # الحقول التي ستظهر في قائمة المستخدمين
    list_display = UserAdmin.list_display + ('date_of_birth',)
    
    # الحقول التي ستظهر عند عرض/تعديل مستخدم موجود
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    # الحقول التي ستظهر عند إنشاء مستخدم جديد في لوحة الإدارة
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

# --- 2. التسجيل (السطر المطلوب) ---
# هذا هو السطر الذي يتوقعه نظام التحقق
admin.site.register(CustomUser, CustomUserAdmin) 

# تسجيل UserProfile أيضاً لتمكين إدارة الأدوار
admin.site.register(UserProfile)