from django.db.models import fields
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
        
class InviteCandidateSerialozer(serializers.ModelSerializer):
    class Meta:
        model = InviteCandidate
        fields = "__all__"

class CandidateWithSpecificDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ("id", "first_name", "last_name", "email", "contact_no")
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        
class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"

# class JobPostSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = JobPost
#         fields = ("id","post_id","job_title","hiring_lead_id", "department_id", "provider_id", "location", "employment_type", "is_mark_remote", "minimum_experience", "job_description", "status", "is_deleted", "created_at", "updated_at")

class ListofJobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ("id", "title")
        


class JobtoapplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ("id","job_title","location","provider_id")
        
class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = "__all__"
        
class InterviewSlotScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSlotSchedule
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
        
        
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"
        
        