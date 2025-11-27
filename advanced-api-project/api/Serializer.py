from rest_framework import serializers 
from .models import Author, Book
from datetime import date 

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Handles serialization of book fields and custom validation for publication_year.
    """
    class meta:
        model = Book
        firlds = '__all__'

    def validate_publication_year(self, value):
        """
        Check that the publication year is not in the future.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication year cannot be in the future.")
        return value
    
    
class Authorserializer(serializers.ModelSerializer):
    """
    serializer for the Author model.
    Includes a nested BookSerializer to display related books dynamically.
    """
    # Nested serializer:
    # many=True: لأن المؤلف قد يكون له أكثر من كتاب
    # read_only=True: لأننا نستخدمه للعرض حالياً، ولتجنب تعقيد الإنشاء في هذه المرحلة
    books = Bookserializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
