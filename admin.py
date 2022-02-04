from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Department)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_deleted', 'created_at', 'updated_at']
# admin.site.register(Department)


@admin.register(Emails)
class EmailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_email', 'to_email', 'subject', 'body', 'attachment', 'status', 'date']
# admin.site.register(Emails)


@admin.register(EmailTemplates)
class EmailTemplatesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject', 'template', 'last_modified_date']
# admin.site.register(EmailTemplates)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'interview_id', 'feedback_value', 'feedback_desc', 'is_deleted', 'created_at', 'updated_at']
# admin.site.register(Feedback)


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'candidate_id', 'job_id', 'hiring_lead_id', 'meeting_type', 'duration', 'additional_information', 'interview_time', 'status', 'is_deleted', 'created_at', 'updated_at']
# admin.site.register(Interview)


@admin.register(InterviewSlotSchedule)
class InterviewSlotScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'interview_date', 'start_time', 'end_time', 'interview_schedule_id', 'is_deleted', 'created_at', 'updated_at']
# admin.site.register(InterviewSlotSchedule)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'interview_id', 'expiry_date', 'join_date', 'pay_rate', 'pay_rate_type', 'offer_letter_pdf', 'mail_subject', 'offered_email', 'status', 'created_at', 'updated_at']
# admin.site.register(Offer)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'contact_no', 'username', 'email', 'user_type', 'department_id', 'domain_name', 'notification_status', 'status', 'is_profile_created', 'is_accepted', 'device_type', 'is_deleted', 'created_at', 'updated_at']
# admin.site.register(User)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'contact_no', 'job_id', 'is_deleted', 'status', 'created_at', 'updated_at']
# admin.site.register(Candidate)


@admin.register(InviteCandidate)
class InviteCandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'contact_no', 'job_id', 'is_deleted', 'created_at', 'updated_at']
# admin.site.register(InviteCandidate)


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_id', 'job_title', 'hiring_lead_id', 'department_id', 'provider_id', 'employment_type', 'is_mark_remote', 'minimum_experience', 'status', 'is_deleted', 'created_at', 'updated_at']
# admin.site.register(JobPost)


# admin.site.register(InterviewSchedule)

