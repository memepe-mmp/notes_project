from django.contrib import admin
from .models import Note, Category, Tag

admin.site.register(Category)
admin.site.register(Tag)
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_done', 'created_at')
    list_filter = ('is_done',)
    search_fields = ('title', 'text')




