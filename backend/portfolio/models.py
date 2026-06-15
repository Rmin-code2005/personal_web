from django.db import models

class Profile(models.Model):
    """اطلاعات کلی — فقط یه رکورد داریم"""
    full_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)        # مثلاً: Backend Developer
    bio = models.TextField()                         # معرفی کلی
    email = models.EmailField()
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)  # آپلود CV

    def __str__(self):
        return self.full_name


class Education(models.Model):
    degree = models.CharField(max_length=200)       # مثلاً: کارشناسی نرم‌افزار
    field = models.CharField(max_length=200)         # مثلاً: مهندسی کامپیوتر
    university = models.CharField(max_length=200)
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)  # null = هنوز در حال تحصیل
    gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.degree} — {self.university}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']  # ← اضافه کن

    def __str__(self):
        return self.name
class Skill(models.Model):
    # CATEGORIES = [
    #     ('backend', 'Backend'),
    #     ('frontend', 'Frontend'),
    #     ('devops', 'DevOps'),
    #     ('Hardware', 'Hardware'),
    #     ('ML' , 'Machine Learning'),
    #     ('AI', 'Artificial Intelligence'),
    #     ('DL', 'Deep Learning'),
    #     ('embedded', 'Embedded Systems'),
    #     ('other', 'Other'),
        
    # ]
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=80)          # 0-100
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , default=None , null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name



class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateField()
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} — {self.sent_at.date()}"