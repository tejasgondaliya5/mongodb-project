from django.db import models
from django.db.models import Model
# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=255, blank=True)  # Department Name
    provider_id = models.IntegerField(blank=True)
    is_deleted = models.CharField(default="0", max_length=1)  # It is Bydefualt 0 and data is Deleted then value is 1
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class User(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    contact_no = models.CharField(max_length=20, blank=True)
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)
    profile_pic = models.ImageField(upload_to="UserProfilePic/", blank=True)
    fcm_token = models.TextField(max_length=1000, blank=True)
    name_of_business = models.CharField(max_length=256, blank=True)
    user_type = models.CharField(max_length=1, blank=True)  # 1 = Admin, 2 = Provider, 3 = hiringLead
    department_id = models.IntegerField(blank=True)
    domain_name = models.CharField(max_length=200, blank=True)
    provider_id = models.IntegerField(blank=True)
    provider_name = models.CharField(max_length=200, blank=True)
    notification_status = models.CharField(default="0", max_length=1, blank=True) #'1 = enable , 0 = disable
    status = models.CharField(default="0", max_length=1, blank=True) #1 = Applied , 2 = Pending , 3 = Pre-Screen , 4 = Approved , 5 = Rejected , 6 = CDL-A Job Request , 7 = Scheduled Interview , 8 = Active , 9 = Schedule OP Interview 
    is_profile_created = models.CharField(default="0", max_length=1, blank=True) # 1 = active , 0 = inactive
    address = models.TextField(max_length=500, blank=True)
    address_2 = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=50, blank=True)
    is_interview = models.CharField(default="1", max_length=1, blank=True) # 0 = true, 1 = false
    is_accepted = models.CharField(default="0", max_length=1, blank=True)
    device_type = models.CharField(default="2", max_length=1, blank=True)  # 0 => ''Android'', 1 => ''IOS'' , 2 => ''Web''
    is_deleted = models.CharField(default="0", max_length=1)  # It is Bydefualt 0 and data is Deleted then value is 1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # address1 = models.TextField(max_length=200,blank=True)
    # address2 = models.TextField(max_length=200, blank=True)
    
    def __str__(self):
        return self.email
    
class Candidate(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    contact_no = models.CharField(max_length=255, blank=True)
    resume =  models.FileField(blank=True, upload_to="Resume/")
    current_company = models.CharField(max_length=500, blank=True)
    is_authorized_work_us = models.CharField(max_length=1, blank=True)   # 0 = no, 1 = yes
    is_require_visa_status = models.CharField(max_length=1, blank=True)  # 0 = no, 1 = yes
    linkedIn_link = models.CharField(max_length=300, blank=True)
    twitter_link = models.CharField(max_length=300, blank=True)
    # github_link = models.CharField(max_length=300, blank=True)
    job_id = models.IntegerField(blank=True)
    provider_id = models.IntegerField(blank=True)
    status = models.CharField(default="1", max_length=1, blank=True)  # 1 = pending , 2 = Waiting , 3 = Processing , 4 = Confirmed , 5 =Completed
    notes = models.TextField(max_length=5000, blank=True)
    is_deleted = models.CharField(default="0", max_length=1)  # It is Bydefualt 0 and data is Deleted then value is 1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # profilePic = models.FileField(blank=True, upload_to="CandidateProfilePic/")
    # status = models.IntegerField(default=1, blank=True) # 1 = pending , 2 = Waiting , 3 = Processing , 4 = Confirmed , 5 =Completed
    
    def __str__(self):
        return self.email
    
class InviteCandidate(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    contact_no = models.CharField(max_length=255, blank=True)
    job_id = models.IntegerField(blank=True)
    provider_id = models.IntegerField(blank=True)
    is_deleted = models.CharField(default="0", max_length=1)  # It is Bydefualt 0 and data is Deleted then value is 1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class JobPost(models.Model):
    post_id = models.CharField(max_length=110, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    hiring_lead_id = models.IntegerField(blank=True)  # used hiringLead table and store data
    provider_id = models.IntegerField(blank=True)
    department_id = models.IntegerField(blank=True)   # user Department model used fo fatch department
    location = models.CharField(max_length=255, blank=True)
    employment_type =models.CharField(default="0", max_length=1, blank=True)  #0 = Day Shift , 1 = Night Shift , 2 = Contract , 3 = Hourly
    is_mark_remote =  models.CharField(default="0", max_length=1)  #0 = unmarked , 1 = marked'
    minimum_experience = models.CharField(max_length=1, blank=True)  # 0 = Entry Level , 1 = Intermediate , 2 = Experienced
    job_description = models.TextField(max_length=10000,blank=True)
    status = models.CharField(default="0", max_length=1, blank=True)  # 0 = open , 1 = closed
    is_deleted = models.CharField(default="0", max_length=1)  # It is Bydefualt 0 and data is Deleted then value is 1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title

class Interview(models.Model):
    candidate_id = models.IntegerField(blank=True)
    job_id = models.IntegerField(blank=True)
    hiring_lead_id = models.IntegerField(blank=True)
    meeting_type = models.CharField(max_length=255, blank=True)
    duration = models.CharField(max_length=255, blank=True)
    additional_information = models.TextField(blank=True,max_length=10000)
    interview_time = models.DateTimeField(blank=True)
    interview_meeting_id = models.CharField(max_length=255, blank=True)
    web_link = models.CharField(max_length=255, blank=True)
    status = models.CharField(default="1", max_length=10, blank=True) # '1 => Pending , 2 => Waiting , 3 => Confirmed , 4 => Processing , 5 => Completed , 6 => Rescheduled, 7 => Rejected , 8 => Cancelled , 9 => offered , 10 => Active(Hired) , 11 => Deleted',
    is_deleted = models.CharField(default="0", max_length=1)  # It is Bydefualt 0 and data is Deleted then value is 1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class Emails(models.Model):
    from_email = models.CharField(max_length=150,blank=True)
    to_email = models.CharField(max_length=100000,blank=True)
    subject = models.CharField(max_length=500, blank=True)
    body = models.TextField(max_length=10000, blank=True)
    attachment = models.CharField(max_length=500)
    status = models.CharField(default="0", max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
    
class EmailTemplates(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=500, blank=True)
    template = models.TextField(max_length=10000, blank=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Feedback(models.Model):
    interview_id = models.IntegerField(blank=True)
    feedback_value = models.CharField(max_length=500, blank=True)
    feedback_desc = models.TextField(max_length=10000, blank=True)
    is_deleted = models.CharField(default="0", max_length=1)  # It is Bydefualt 0 and data is Deleted then value is 1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.interview_id
    

class InterviewSlotSchedule(models.Model):
    interview_date = models.DateField(blank=True)
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    interview_schedule_id = models.IntegerField(blank=True)
    is_deleted = models.CharField(default="0", max_length=1)  # It is Bydefualt 0 and data is Deleted then value is 1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def __str__(self):
    #     return self.interview_schedule_id
    

class Offer(models.Model):
    interview_id = models.IntegerField(blank=True)
    expiry_date = models.DateField(blank=True)
    join_date = models.DateField(blank=True)
    pay_rate = models.CharField(max_length=155, blank=True)
    pay_rate_type = models.CharField(max_length=155, blank=True)
    offer_letter_pdf= models.CharField(max_length=500, blank=True)
    mail_subject = models.CharField(max_length=255, blank=True)
    mail_content = models.TextField(blank=True,max_length=5000)
    offered_email = models.CharField(max_length=255, blank=True)
    status = models.CharField(default="1",max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.interview_id



    