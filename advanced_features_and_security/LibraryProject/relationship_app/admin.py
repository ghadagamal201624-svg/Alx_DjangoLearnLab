from django.contrib import admin
# Register your models here.

# relationship_app/admin.py
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

# --- Custom Admin Model for CustomUser ---
class CustomUserAdmin(UserAdmin):
    # الحقول التي ستظهر في قائمة المستخدمين
    list_display = UserAdmin.list_display + ('date_of_birth',)
    
    # الحقول التي ستظهر عند عرض/تعديل مستخدم موجود
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    # الحقول التي ستظهر عند إنشاء مستخدم جديد
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'date_of_birth', 'profile_photo')}),
    )

# إلغاء تسجيل النموذج الافتراضي (إذا كان مسجلاً) وتسجيل النموذج المخصص
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)