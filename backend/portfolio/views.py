from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Education, Skill, Project, ContactMessage
from .serializers import (
    ProfileSerializer, EducationSerializer,
    SkillSerializer, ProjectSerializer, ContactMessageSerializer
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

class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ContactCreateView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'پیامت دریافت شد!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)