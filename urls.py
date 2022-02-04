from django.urls import path, include
from . import views
urlpatterns = [
    path('user_signin', views.user_signin),
    
    path('add_department', views.add_department),
    path('get_all_department', views.get_all_department),
    path('delete_department', views.delete_department),
    
    
    path('create_user', views.create_user),
    path('get_register_user', views.get_register_user),
    path('get_user_by_department_id', views.get_user_by_department_id),
    path('delete_user', views.delete_user),
    
    
    path('create_job_post', views.create_job_post),
    path('re_create_job_post', views.re_create_job_post),
    path('get_all_job_posts', views.get_all_job_posts),
    path('get_job_by_id', views.get_job_by_id),
    path('delete_job_post_by_id', views.delete_job_post_by_id),

    
    path('invite_candidate', views.invite_candidate),
    path('create_candidate', views.create_candidate),
    path('get_candidate', views.get_candidate),
    path('get_candidate_by_id', views.get_candidate_by_id),
    path('change_candidate_status', views.change_candidate_status),
    path('get_jobs_to_apply', views.get_jobs_to_apply),
    

    path('request_interview', views.request_interview),
    path('change_interview_status', views.change_interview_status),
    path('get_hiring_lead_interviews', views.get_hiring_lead_interviews),
    path('create_interview_schedule', views.create_interview_schedule),
    path('get_interview_by_id', views.get_interview_by_id),
    path('get_interview_for_candidate', views.get_interview_for_candidate),
    path('start_interview_process', views.start_interview_process),
    path('accept_interview_schedule', views.accept_interview_schedule),
    path('get_hiring_lead_interviews', views.get_hiring_lead_interviews),
    
    
    path('create_feedback', views.create_feedback),


    path('offer_candidate', views.offer_candidate),
    path('change_offer_status', views.change_offer_status),
    
    # path('get_list_jobs', views.get_list_jobs),
    
    # path('test_pdf', views.test_pdf),
    # path('pdf', views.CreatePdf),
]