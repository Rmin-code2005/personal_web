from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Education, Skill, Project, ContactMessage, Category
from .serializers import (
    ProfileSerializer, EducationSerializer,
    SkillSerializer, ProjectSerializer, ContactMessageSerializer,
    CategorySerializer,
)


class ProfileView(APIView):
    """همیشه فقط یه پروفایل داریم"""
    def get(self, request):
        profile = Profile.objects.first()
        if not profile:
            return Response({'detail': 'پروفایل تنظیم نشده'}, status=404)
        return Response(ProfileSerializer(profile).data)


class EducationListView(generics.ListAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class CategoryListView(generics.ListAPIView):
    """لیست همه دسته‌بندی‌های مهارت"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all().select_related('category')
    serializer_class = SkillSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # فیلتر اختیاری روی category: /api/skills/?category=1
        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # فیلتر اختیاری: /api/projects/?featured=true
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            qs = qs.filter(is_featured=True)
        return qs


class ContactCreateView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'پیامت دریافت شد!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)