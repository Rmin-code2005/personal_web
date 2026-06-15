from rest_framework import serializers
from .models import Profile, Education, Skill, Project, ContactMessage, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    is_current = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = '__all__'

    def get_is_current(self, obj):
        return obj.end_year is None  # اگه end_year نداشت یعنی هنوز داره می‌خونه


class SkillSerializer(serializers.ModelSerializer):
    # اطلاعات کامل category رو نشون میده (read-only)
    category = CategorySerializer(read_only=True)
    # برای نوشتن (POST/PUT) فقط id کافیه
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Skill
        fields = ['id', 'name', 'level', 'order', 'category', 'category_id']


class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_tech_list(self, obj):
        # "Python, Django, React" → ["Python", "Django", "React"]
        return [t.strip() for t in obj.tech_stack.split(',')]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']