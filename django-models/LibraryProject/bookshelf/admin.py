from django.contrib import admin
from .models import Book 

class BookAdmin(admin.ModelAdmin):
    # table colum 
    list_display = ('title', 'author', 'publication_year')
    
    # 2.search 
    search_fields = ('title', 'author')
    
    # 3.filter
    list_filter = ('publication_year',)


admin.site.register(Book, BookAdmin)