from django.contrib import admin
from .models import Profile, Education, Skill, Project, ContactMessage, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'email']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'field', 'university', 'start_year', 'end_year']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'created_at']
    list_editable = ['is_featured']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'level', 'order']
    list_editable = ['order', 'level']
    list_filter = ['category']          # فیلتر کنار صفحه بر اساس دسته‌بندی
    search_fields = ['name']
    autocomplete_fields = ['category']  # برای انتخاب راحت‌تر category در فرم


@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'sent_at', 'is_read']
    list_filter = ['is_read']
    readonly_fields = ['sent_at']