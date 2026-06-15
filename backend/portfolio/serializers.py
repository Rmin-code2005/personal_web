from rest_framework import serializers
from .models import Profile, Education, Skill, Project, ContactMessage

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
    class Meta:
        model = Skill
        fields = '__all__'

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