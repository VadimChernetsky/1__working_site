from django.contrib import admin
from .models import Video, AdditionalImage, Category


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'content', 'image', 'is_active', 'price', 'url', 'created_dt', 'categ')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    inlines = (AdditionalImageInline,)
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ('is_active',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)