from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from .ResponsFile import *
from django.core.paginator import Paginator
import hashlib
from .createpdf import create_pdf
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from .curl import *
from django.conf import settings

# Create your views here.

@api_view(['POST'])
def user_signin(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            jsondata["password"] = hashlib.sha256(jsondata["password"].encode()).hexdigest()
            try:
                data = User.objects.get(username = jsondata["username"], password = jsondata["password"], is_deleted="0")
                serializer = UserSerializer(data)
                return Response(getResponseByType("Success", "Create Signin success.", "Create Signin API", "Create Signin API", "Userdata", serializer.data))
            
            except:
                try:
                    data = User.objects.get(email = jsondata["email"], password = jsondata["password"], is_deleted="0")
                    serializer = UserSerializer(data)
                    return Response(getResponseByType("Success", "Create Signin success.", "Create Signin API", "Create Signin API", "Userdata", serializer.data))
                except:
                    return Response(getResponseByType("Fail", "Invalid Username or password, please try again.", "Create Signin API", "Create Signin API", "Value", "Invalid username or email, please try again."))
        
        else:
            return Response(getResponseByType("Fail", "Username or password is must, please try again.", "Create Signin API", "Create Signin API", "Value", "Username or password is must, please try again."))


# Department data
@api_view(['POST'])
def add_department(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                if jsondata["is_created"]=="1":
                    try:
                        get_id = Department.objects.get(id=jsondata["id"])
                        serializers = DepartmentSerializer(get_id, data=jsondata, partial=True)
                        if serializers.is_valid():
                            serializers.save()
                            return Response(getResponseByType("Success", "Department update successfully", "Update Department API", "Update Department API", "Departmentdata", serializers.data))
                            
                        return Response(getResponseByType("Fail", "fail Department data", "update Department API", "Update Department API", "data", serializers.errors))
                        
                    except Exception as e:
                        return Response(getResponseByType("Fail", "Department    '_id' is not match", "update Department API", f"Update Department API{e}"))

                elif jsondata["is_created"]=="0":
                    validate = Department.objects.filter(name=jsondata["name"])
                    if len(validate)>=1:
                        return Response(getResponseByType("Fail", "Department already exists", "Create add Department API", "Create add Department API", "Value", "Department already exists"))

                    else:
                        serializers = DepartmentSerializer(data=jsondata)
                        if serializers.is_valid():
                            serializers.save()
                            Departmentdata = Department.objects.get(name=jsondata["name"])
                            serializers = DepartmentSerializer(Departmentdata)
                            return Response(getResponseByType("Success", "Add Department Success", "Add Department API", "Add Department API", "Departmentdata", serializers.data))
                        else:
                            return Response(getResponseByType("Fail", "Department Data is Invalid", "Create add Department API", "Create add Department API", "data", serializers.errors))
            except Exception as e:
                return Response(getResponseByType("Fail", "Invalid is_created", "Create add Department API", f"Create add Department API{e}"))
    else:
        return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Create add or update Department API", "Create add or update Department API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def get_all_department(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
        try:
            try:
                get_Department=list(reversed(Department.objects.filter(provider_id=jsondata["provider_id"], is_deleted="0")))
                if len(get_Department)>0:
                    serializers = DepartmentSerializer(get_Department, many=True)
                    for i in range(0, len(serializers.data)):
                        try:
                            # get provider name
                            get_provider_name = User.objects.get(id=get_Department.provider_id)
                            serializers.data[i]["provider_name"]=get_provider_name.provider_name
                        except Exception as e:
                            serializers.data[i]["provider_name"]=""
                    return Response(getResponseByType("Success", "get Department with id data successfully", "Get Department Data API", "Get Deparment By Id", "data", serializers.data))
                
            except Exception as e:
                pass
            
            get_Department=Department.objects.get(id=jsondata["id"], is_deleted="0")
            serializers = DepartmentSerializer(get_Department)
            serializers = serializers.data
            
            try:
                # get provider name
                get_provider_name = User.objects.get(id=get_Department.provider_id)
                serializers["provider_name"]=get_provider_name.provider_name
            except:
                serializers["provider_name"] = ""
                
                
            return Response(getResponseByType("Success", "get Department with id data successfully", "Get Department Data API", "Get Deparment By Id", "data", serializers))
        
        except:
            try:
                get_Department = list(reversed(Department.objects.filter(is_deleted="0")))
                serializers = DepartmentSerializer(get_Department, many=True)
                for i in range(0, len(serializers.data)):
                    try:
                        get_provider_name = User.objects.get(id=get_Department[i].provider_id)
                        serializers.data[i]["provider_name"]=get_provider_name.provider_name
                    except:
                        serializers.data[i]["provider_name"]=""
                return Response(getResponseByType("Success", "get Department data successfully", "Get Department Data API", "Deparment All data", "data", serializers.data))
            except Exception as e:
                return Response(getResponseByType("Fail", "get Department data Fail", "Get Department Data API", "Deparment All data", "Value", f"get Department data Fail, {e}"))


@api_view(['POST'])
def delete_department(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_Department = Department.objects.get(id=jsondata["id"])
                get_Department.is_deleted = "1"
                get_Department.save()
                return Response(getResponseByType("Success", "Department data is Deleted", "Delete Department API", "Department data is Deleted By id", "Value", "Delete Department Success"))
            except Exception as e:
                return Response(getResponseByType("Fail", "invalid id", "Delete Department API", "Department data is Deleted By id", "Value", f"invalid Department _id, {e}"))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Delete Department API", "Delete Department API", "Value", "insert valid data is reqired, please try again."))


# user data
@api_view(['POST'])
def create_user(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                jsondata["profile_pic"] = request.data["profile_pic"]
            except Exception as e:
                pass
            try:
                if jsondata["is_created"]=="1":
                    try:
                        data = User.objects.get(id=jsondata["id"])
                        serializers = UserSerializer(data, data=jsondata, partial=True)
                        if serializers.is_valid():
                            serializers.save()
                            serializer = UserSerializer(data)
                            return Response(getResponseByType("Success", "updated User successfully", "Update user API", "Update user API", "Userdata", serializer.data))
                        return Response(getResponseByType("Fail", "Invalid data", "Update user API", "Update user API", "data", serializers.errors))
                    except Exception as e:
                        return Response(getResponseByType("Fail", "invalid user data _id", "Update user API", "create user API", "Value", f"invalid user data _id, {e}"))

                elif jsondata["is_created"]=="0":
                    validate = User.objects.filter(contact_no=jsondata["contact_no"])
                    if len(validate)>0:
                        return Response(getResponseByType("Fail", "This Contact Number is already exists.", "Create User API", "Create User API", "Value", "This Contact Number is already exists."))
                    
                    validate = User.objects.filter(email=jsondata["email"])
                    if len(validate)>0:
                        return Response(getResponseByType("Fail", "This Email Id is already exists.", "Create User API", "Create User API", "Value", "This Email Id is already exists."))
                    
                    else:
                        try:
                            jsondata["password"] = hashlib.sha256(jsondata["password"].encode()).hexdigest()
                        except Exception as e:
                            print("e")
                        serializer = UserSerializer(data=jsondata)
                        if serializer.is_valid():
                            serializer.save()
                            user_data = User.objects.get(email=jsondata["email"])
                            serializers = UserSerializer(user_data)
                            return Response(getResponseByType("Success", "Create User Success.", "Create User API", "Create User API", "Userdata", serializers.data))
                        return Response(getResponseByType("Fail", "Invalid Data", "create user API", "Create User API", "data", serializer.errors))
                    
                else:
                    return Response(getResponseByType("Fail", "Invalid is_created", "create user API", "create user API", "Value", "invalid user data _id"))
            except Exception as e:
                return Response(getResponseByType("Fail", "Invalid is_created", "create user API", "create user API", "Value", f"invalid user data _id, {e}"))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "create user API", "create user API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def get_register_user(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                candidate = User.objects.get(id=jsondata["id"])
                serializers = UserSerializer(candidate)
                return Response(getResponseByType("Success", "Get User Data by id Success", "Get User Data API", "Get User Data API", "data", serializers.data))
            
            except:
                try:
                    candidate = list(reversed(User.objects.filter(user_type=jsondata["user_type"], is_deleted="0")))
                    if len(candidate)>0:
                        serializers = UserSerializer(candidate, many=True)
                        for i in range(0, len(candidate)):
                            serializers.data[i]["fullName"]=candidate[i].first_name+" "+candidate[i].last_name
                            try:
                                data = Department.objects.get(id=serializers.data[i]["department_id"], is_deleted="0")
                                serializers.data[i]["department_name"]=data.name
                            except Exception as e:
                                serializers.data[i]["department_name"]=""
                            if jsondata["user_type"]=="3":
                                try:
                                    provider = User.objects.get(id=serializers.data[i]["provider_id"], is_deleted="0")
                                    serializers.data[i]["provider_name"]=provider.provider_name
                                except Exception as e:
                                    serializers.data[i]["provider_name"]=""
                                
                        return Response(getResponseByType("Success", "Get User Data Success", "Get User Data API", "Get User Data API", "data", serializers.data))
                    else:
                        return Response(getResponseByType("Fail", "Get User Data Fail", "Get User Data API", "Get User Data API", "Value", " Invalid user_type."))
                except Exception as e:
                    return Response(getResponseByType("Fail", "Get User Data Fail", "Get User Data API", "Get User Data API", "Value", f" Invalid user_type. {e}"))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Get User Data API", "Get User Data API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def get_user_by_department_id(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            if jsondata:
                try:
                    data = list(reversed(User.objects.filter(department_id=jsondata["department_id"], is_deleted="0")))
                    if len(data)>=1:  # becuse data can show empty Queryset objects value 
                        serializers = UserSerializer(data, many=True)
                        for i in range(0, len(serializers.data)):
                            serializers.data[i]["fullName"]= data[i].first_name+" "+data[i].last_name
                            
                        return Response(getResponseByType("Success", "Get User By Department Success.", "Get User By Department Data API", "Get User By Department Data API", "data", serializers.data))
                    else:
                        return Response(getResponseByType("Fail", "Get User By Department Data Fail", "Get User By Department Data API", "Get User By Department Data API", "Value", "Get User By Department Data Fail."))
                except Exception as e:
                    return Response(getResponseByType("Fail", "Get User By Department Data Fail", "Get User By Department Data API", "Get User By Department Data API", "Value", "Get User By Department Data Fail."))
            else:
                return Response(getResponseByType("Fail", "Get User By Department Data Fail.", "Get User By Department Data API", "Get User By Department Data API", "Value", "Get User By Department Data Fail."))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Get User By Department Data API", "Get User By Department Data API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def delete_user(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_user = User.objects.get(id=jsondata["id"])
                get_user.is_deleted = "1"
                get_user.save()
                return Response(getResponseByType("Success", "Delete User Success", "Delete User API", "Delete User API", "Value", "Delete User Success."))
            except:
                return Response(getResponseByType("Fail", "invalid id", "Delete User API", "Delete User API", "Value", "Delete User Fail."))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Delete User API", "Delete User API", "Value", "insert valid data is reqired, please try again."))


# Jobpost data
@api_view(['POST'])
def create_job_post(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                if jsondata["is_created"]=="1":
                    try:
                        data = JobPost.objects.get(id=jsondata["id"])
                        serializers = JobPostSerializer(data, data=jsondata, partial=True)
                        if serializers.is_valid():
                            serializers.save()
                            return Response(getResponseByType("Success", "updated Jobpost successfully", "Create Job Post API", "Create Job Post API", "data", "success Job Post Update"))
                        return Response(getResponseByType("Fail","Jobpost Data is Invalid" , "Update Job Post API", "Update Job Post API", "data", serializers.errors))
                
                    except:
                        return Response(getResponseByType("Fail","JobPost '_id' is Fail" , "Create Job Post API", "Create Job Post API", "Value", "Fail JobPost _id"))
                    
                elif jsondata["is_created"]=="0":
                    # this code is add custome id
                    try:
                        custom_id = JobPost.objects.latest('id')
                        if len(format(custom_id.id))==1:
                            jsondata["post_id"]= f"TKJ-10{custom_id.id+1}"
                        elif len(format(custom_id.id))==2:
                            jsondata["post_id"]= f"TKJ-1{custom_id.id+1}"
                        else:
                            jsondata["post_id"]= f"TKJ-{custom_id.id+1}"
                    except:
                        # jsondata["post_id"] = "TKJ-101"
                        pass
                        
                    # normal code start
                    serializer = JobPostSerializer(data=jsondata)
                    if serializer.is_valid():
                        serializer.save()
                        try:
                            get_job_id = JobPost.objects.get(job_title=jsondata["job_title"], hiring_lead_id=jsondata["hiring_lead_id"], is_deleted="0")
                            if get_job_id.post_id:
                                pass
                            else:
                                if len(format(get_job_id.id))==1:
                                    get_job_id.post_id= f"TKJ-10{get_job_id.id}"
                                elif len(format(get_job_id.id))==2:
                                    get_job_id.post_id= f"TKJ-1{get_job_id.id}"
                                else:
                                    get_job_id.post_id= f"TKJ-{get_job_id.id}"
                            get_job_id.save()
                        
                        except:
                            pass
                            
                        return Response(getResponseByType("Success", "Create Job Post success.", "Create Job Post API", "Create Job Post API", "data", "Job Post success"))
                    else:
                        return Response(getResponseByType("Fail","Fail Job Post Create." , "Create Job Post API", "create Job Post API", "data", serializer.errors))
                    
                else:
                    return Response(getResponseByType("Fail","Invalid is_created" , "Create Job Post API", "Create Job Post API", "Value", "Invalid is_created"))

            except Exception as e:
                return Response(getResponseByType("Fail","Insert valid is_created" , "create user API", "create user API", "Value", f"Invalid is_created,{e}"))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "create and update user API", "create and update user API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def get_all_job_posts(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_jobpost = list(reversed(JobPost.objects.filter(status=jsondata["status"], is_deleted="0")))
                if len(get_jobpost) >=1:
                    serializers = JobPostSerializer(get_jobpost, many=True)
                    for i in range(len(serializers.data)):
                        
                        serializers.data[i]["candidates"]=str(len(Candidate.objects.filter(job_id=get_jobpost[i].id, is_deleted="0")))
                        
                        hiring_lead_name = User.objects.get(id=get_jobpost[i].hiring_lead_id, is_deleted="0")
                        serializers.data[i]["hiring_lead_name"]= hiring_lead_name.first_name+" "+hiring_lead_name.last_name
                        if serializers.data[i]["provider_id"]:
                            try:
                                get_provider_name = User.objects.get(id=get_jobpost[i].provider_id, is_deleted="0")
                                serializers.data[i]["provider_name"] =  get_provider_name.provider_name
                            except Exception as e:
                                print(e)
                        
                        serializers.data[i]["employment_type_name"]= employment_type(get_jobpost[i].employment_type)
                        
                        serializers.data[i]["minimum_experience_type"]=minimum_experience(get_jobpost[i].minimum_experience)
                        
                        serializers.data[i]["status_name"]=status_name(get_jobpost[i].status)
                        
                    return Response(getResponseByType("Success", "Get Job success", "get all job API", "get all job API", "data", serializers.data))
                else:
                    return Response(getResponseByType("Fail", "Get Job success But data is empty.", "get all job API", "get all job API", "value", "Get Job success But data is empty."))
                    
            except Exception as e:
                return Response(getResponseByType("Fail","Invalid status, please try again." , "get all job API", "get all job API", "Value", f"Invalid status, {e}"))
            
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "get all job API", "get all job API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def get_job_by_id(request):
    if request.method =="POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_job = JobPost.objects.get(id=jsondata["id"], is_deleted="0")
                serializers = JobPostSerializer(get_job) # filter use because data is not change after serializer
                data = serializers.data
                if get_job.hiring_lead_id:
                    hiring_lead_name = User.objects.get(id=(get_job.hiring_lead_id))
                    data["hiring_lead_name"]= hiring_lead_name.first_name+" "+hiring_lead_name.last_name
                
                data["employment_type_name"]= employment_type(get_job.employment_type)
                
                if get_job.provider_id:
                    get_provider_name = User.objects.get(id=get_job.provider_id, is_deleted="0")
                    data["provider_name"]= get_provider_name.provider_name
                
                data["status_name"]=status_name(get_job.status)
                
                return Response(getResponseByType("Success", "Get Job success", "Get Job API", "Get Job API", "data", data))
                
            except Exception as e:
                return Response(getResponseByType("Fail","Invalid id, please try again." , "Get Job API", "Get Job API", "Value", f"Invalid status, {e}"))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Get Job API", "Get Job API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def delete_job_post_by_id(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_Jobpost = JobPost.objects.get(id=jsondata["id"])
                get_Jobpost.is_deleted = "1"
                get_Jobpost.save()
                return Response(getResponseByType("Success", "Delete Job success.", "Delete Job API", "Delete Job API", "Value", "Delete Job success."))
            except Exception as e:
                return Response(getResponseByType("Fail", "invalid id.", "Delete Job API", "Delete Job API", "Value", f"invalid id, {e}"))
        
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Delete Job API", "Delete Job API", "Value", "insert valid data is reqired, please try again."))

@api_view(['POST'])
def invite_candidate(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            if jsondata["is_created"]=="0":
                
                validate = InviteCandidate.objects.filter(contact_no=jsondata["contact_no"])
                if len(validate)>0:
                    return Response(getResponseByType("Fail", "contectNo is already exists", "Create Invited Candidate API", "Create Invited Candidate API", "Value", "contectNo is already exists"))

                validate = InviteCandidate.objects.filter(email=jsondata["email"])
                if len(validate)>0:
                    return Response(getResponseByType("Fail", "email is already exists", "Create Invited Candidate API", "Create Invited Candidate API", "Value", "email is already exists"))

                else:
                    serializers = InviteCandidateSerialozer(data=jsondata)
                    if serializers.is_valid():
                        serializers.save()
                        
                        # Save Email
                        get_provider = User.objects.get(id=jsondata["provider_id"])
                        
                        get_invite_candidate_template = EmailTemplates.objects.get(name="invite_candidate")
                        html = f"{get_invite_candidate_template.template}"
                        html = html.replace("first_name", jsondata["first_name"]).replace("last_name", jsondata["last_name"]).replace("web_link", get_provider.domain_name)
                        
                        obj = Emails()
                        obj.from_email = "hello@trukyn.com"
                        obj.to_email = jsondata["email"]
                        obj.subject = get_invite_candidate_template.subject
                        obj.body = html
                        obj.attachment = "File"
                        obj.save()
                        
                        return Response(getResponseByType("Success", "Create Invited Candidate Success.", "Create Invited Candidate API", "Create Invited Candidate API", "Value", "Create Invited Candidate Success."))

                    return Response(getResponseByType("Fail", "Create Invited Candidate Fail", "Create Invited Candidate API", "Create Invited Candidate API", "Value", f"Create Invited Candidate Fail. {serializers.errors}"))

            elif jsondata["is_created"]=="1":
                try:
                    InviteCandidate_id = InviteCandidate.objects.get(id=jsondata["id"], is_deleted="0")
                    serializers = InviteCandidateSerialozer(InviteCandidate_id, data=jsondata, partial=True)
                    if serializers.is_valid():
                        serializers.save()
                        serializers = InviteCandidateSerialozer(InviteCandidate_id)
                        return Response(getResponseByType("Success", "Update Invited Candidate Success.", "Update Invited Candidate API", "Update Invited Candidate API", "data", serializers.data))

                    return Response(getResponseByType("Fail", "Update Invited Candidate Success.", "Update Invited Candidate API", "UPdate Invited Candidate API", "Value", f"Update Invited Candidate Fail. {serializers.errors}"))

                except Exception as e:
                    return Response(getResponseByType("Fail", "Create Invited Candidate Fail", "Create Invited Candidate API", "Create Invited Candidate API", "Value", f"Create Invited Candidate Fail,{e}"))

            else:
                return Response(getResponseByType("Fail","Insert valid is_created" , "Create/Update Invited Candidate API", "Create/Update Invited Candidate API", "Value", "Invalid is_created"))
                
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Create/Update Invited Candidate API", "Create/Update Invited Candidate API", "Value", "insert valid data is reqired, please try again."))


# candidate 
@api_view(['POST'])
def create_candidate(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                jsondata["resume"] = request.data["resume"]
            except:
                pass
            try:
                validate = Candidate.objects.filter(contact_no=jsondata["contact_no"])
                if len(validate)>=1:
                    return Response(getResponseByType("Fail", "contectNo is already exists", "Create User API", "Create User API", "Value", "contectNo is already exists"))
                
                validate = Candidate.objects.filter(email=jsondata["email"])
                if len(validate)>=1:
                    return Response(getResponseByType("Fail", "email is already exists", "Create User API", "Create User API", "Value", "email is already exists"))
                
                else:
                    serializers = CandidateSerializer(data=jsondata)
                    if serializers.is_valid():
                        serializers.save()
                        return Response(getResponseByType("Success", "Create Candidate Success.", "Create Candidate API", "Create Candidate API", "data", "success Job Post Update"))

                    return Response(getResponseByType("Fail","Fail Create Candidate API" , "Create Candidate API", "Create Candidate API", "data", serializers.errors))

            except Exception as e:
                return Response(getResponseByType("Fail","Create Candidate Fail." , "Create Candidate API", "Create Candidate API", "Value", f"Create Candidate Fail.{e}"))
        
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Create or update Candidate API", "Create or Update Candidate API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST',])
def get_candidate(request):
    if request.method =="POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                jsondata["is_pagination"]=jsondata["is_pagination"]
            except:
                jsondata["is_pagination"]="0"
                
            try:
                if jsondata["is_pagination"]=="1":
                    try:
                        get_candidate = list(reversed(Candidate.objects.filter(status=jsondata["status"], is_deleted="0")))
                        
                        serializers = CandidateSerializer(get_candidate, many=True)
                        
                        return Response(getResponseByType("Success", "get candidate success", "get candidate API", "get candidate API", "data", serializers.data))
                    except Exception as e:
                        return Response(getResponseByType("Fail", "Invalid data.", "get candidate API", "get candidate API", "Value", f"invalid id, {e}"))
                else:
                    try:
                        get_candidate = list(reversed(Candidate.objects.filter(status=jsondata["status"], job_id=jsondata["job_id"], is_deleted="0")))
                        if len(get_candidate)>=1:
                            try:
                                parPage = int(jsondata["parPage"])
                            except:
                                parPage = 10
                            # belove line is declear pagination in get candidate
                            paginator = Paginator(get_candidate, parPage)
                            
                            try:
                                page_obj = paginator.get_page(jsondata["page"])
                            except:
                                page_obj = paginator.get_page(1)
                            
                            # -------set totalpage value---------
                            totalpage=len(get_candidate)%parPage
                            if totalpage==0:
                                totalpage = int(len(get_candidate)//parPage)
                            else:
                                totalpage = int(len(get_candidate)//parPage)+1
            
                            
                            serializers = CandidateWithSpecificDataSerializer(page_obj, many=True)
                            for i in range(0,(len(serializers.data))):
                                serializers.data[i]["fullName"]=serializers.data[i]["first_name"]+" "+serializers.data[i]["last_name"]
                            
                            try:
                                currentpage = int(jsondata["page"])
                            except:
                                currentpage = 1
                                
                            return Response(getResponseByTypewithpagination("Success", "get candidate success", "get candidate API", "get candidate API", "data", serializers.data,len(get_candidate), totalpage, currentpage, parPage))

                        
                        else:
                            return Response(getResponseByType("Fail", "get candidate success but data is Empty", "get candidate API", "get candidate API", "value","get candidate success but data is Empty"))
                        
                    except Exception as e:
                        return Response(getResponseByType("Fail", "Invalid data.", "get candidate API", "get candidate API", "Value", f"invalid id,{e}"))
            
            except Exception as e:
                return Response(getResponseByType("Fail", "insert valid data is reqired.", "get candidate API", "get candidate API", "Value", f"invalid id, {e}"))

        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired.", "get candidate API", "get candidate API", "Value", "invalid id."))


@api_view(['POST'])
def get_candidate_by_id(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                detail = Candidate.objects.get(id=jsondata["id"], is_deleted="0")
                serializers = CandidateSerializer(detail)
                data = serializers.data
                data["fullName"] = detail.first_name+" "+detail.last_name
                
                try:
                    interview_data = Interview.objects.get(candidate_id = jsondata["id"], is_deleted="0")
                    if interview_data.interview_time != None:
                        interview_data.interview_time=interview_data.interview_time.strftime("%Y-%m-%d %H:%M:%S")
                    serializers = InterviewSerializer(interview_data)
                    data["interview"]=serializers.data
                except:
                    data["interview"]={}
                
                try:
                    interview_slot = InterviewSlotSchedule.objects.filter(interview_schedule_id=interview_data.id, is_deleted="0")
                    serializers = InterviewSlotScheduleSerializer(interview_slot, many=True)
                    data["interview"]["interview_slot"]=serializers.data
                except:
                    data["interview"]["interview_slot"]=[]
                    
                try:
                    get_job_title = JobPost.objects.get(id = detail.job_id, is_deleted="0")
                    data["interview"]["job_title"]=get_job_title.job_title
                except:
                    data["interview"]["job_title"]=""
                    
                try:
                    get_hiringlead_name = User.objects.get(id=get_job_title.hiring_lead_id)
                    data["interview"]["hiring_lead_name"]=get_hiringlead_name.first_name+" "+get_hiringlead_name.last_name
                except:
                    data["interview"]["hiring_lead_name"]=""
                    
                try:
                    data["interview"]["status_name"]=intreview_status_name(interview_data.status)
                except:
                    data["interview"]["status_name"]=""
                
                try:
                    get_feedback = Feedback.objects.get(interview_id=interview_data.id)
                    serializers =FeedbackSerializer(get_feedback)
                    data["feedback"]=serializers.data
                except:
                    data["feedback"]=None
                
                try:
                    get_offer_data = Offer.objects.filter(interview_id=interview_data.id)
                    serializers = OfferSerializer(get_offer_data, many=True)
                    data["offer_data"]=serializers.data
                except:
                    data["offer_data"]=[]
                    
                
                return Response(getResponseByType("Success", "Get Candidate Success.", "Get Candidate API", "Get Candidate API", "data", data))
            except:
                return Response(getResponseByType("Fail", "Fail Get Candidate.", "Get Candidate API", "Get Candidate API", "value", "Fail Get Candidate."))
        
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Get Candidate API", "Get Candidate API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def change_candidate_status(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_candidate = Candidate.objects.get(id=jsondata["id"], is_deleted="0")
                get_candidate.status = jsondata["status"]
                get_candidate.save()
                return Response(getResponseByType("Success", "Change Candidate Status Success.", "Change Candidate Status API", "Change Candidate Status API", "value", "Change Candidate Status Success"))
            except:
                return Response(getResponseByType("Fail", "Change Candidate Status Fail.", "Change Candidate Status API", "Change Candidate Status API", "value", "Fail Get Candidate."))
        
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Change Candidate Status API", "Change Candidate Status API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def get_jobs_to_apply(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                jsondata["is_pagination"]=jsondata["is_pagination"]
            except:
                jsondata["is_pagination"]="0"
            
            try:
                if jsondata["is_pagination"]=="1":
                    try:
                        get_jobpost =  list(reversed(JobPost.objects.filter(status = jsondata["status"],is_deleted="0")))
                        serializers = JobtoapplaySerializer(get_jobpost, many=True)
                        
                        i=0
                        for data in get_jobpost:
                            serializers.data[i]["employment_type_name"]= employment_type(data.employment_type)
                            serializers.data[i]["minimum_experience_type"]= minimum_experience(data.minimum_experience)
                            
                            i+=1
                        return Response(getResponseByType("Success", "Job post found", "Search Job Post API", "Search Job Post API", "data", serializers.data))
                    except:
                        return Response(getResponseByType("Fail", "Invalid data.", "get candidate API", "get candidate API", "Value", "invalid id."))
                
                else:
                    try:
                        get_jobpost = list(reversed(JobPost.objects.filter(status=jsondata["status"], is_deleted="0")))
                        if len(get_jobpost)>=1:
                            try:
                                parPage = int(jsondata["parPage"])
                            except:
                                parPage = 10
                            paginator = Paginator(get_jobpost, parPage)
                            try:
                                page_obj = paginator.get_page(jsondata["page"])
                            except:
                                page_obj = paginator.get_page(1)
                            
                            # -------set totalpage value---------
                            totalpage=len(get_jobpost)%parPage
                            if totalpage==0:
                                totalpage = int(len(get_jobpost)//parPage)
                            else:
                                totalpage = int(len(get_jobpost)//parPage)+1
                            serializers = JobtoapplaySerializer(page_obj, many=True)
                            i=0
                            get_jobpost_detail = JobPost.objects.get(id=serializers.data[0]["id"])
                            for i in range(len(serializers.data)):
                                serializers.data[i]["employment_type_name"] = employment_type(get_jobpost_detail.employment_type)
                                serializers.data[i]["minimum_experience_type"] = minimum_experience(get_jobpost_detail.minimum_experience)
                                i+=1
                            # -------set currentpage value---------
                            try:
                                currentpage = int(jsondata["page"])
                            except:
                                currentpage = 1
                            return Response(getResponseByTypewithpagination("Success", "Job post found", "Search Job Post API", "Search Job Post API", "data", serializers.data, len(get_jobpost), totalpage, currentpage, parPage))
                        
                        else:
                            return Response(getResponseByType("Fail", "Job post found success but data is Empty", "Search Job Post API", "Search Job Post API", "value","Job post found success but data is Empty"))
                        
                    except:
                        return Response(getResponseByType("Fail", "Invalid data.", "Search Job Post API", "Search Job Post API", "Value", "invalid id."))

            except:
                return Response(getResponseByType("Fail", "insert valid data is reqired.", "Search Job Post API", "Search Job Post API", "Value", "invalid id."))
            
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired.", "Search Job Post API", "Search Job Post API", "Value", "invalid id."))


@api_view(['POST'])
def re_create_job_post(request):
    if request.method == 'POST':
        if request.data:
            jsondata = eval(request.data["data"])

            try:
                get_jobpost = JobPost.objects.get(id=jsondata["id"], is_deleted="0")
                get_jobpost.status = "0"
                new_jobpost = JobPostSerializer(get_jobpost)
                serializers = JobPostSerializer(data=new_jobpost.data)
                if serializers.is_valid():
                    serializers.save()
                    return Response(getResponseByType("Success", "Change Jobpost Status Success.", "Change Candidate Jobpost API", "Change Jobpost Status API", "data", serializers.data))

                return Response(getResponseByType("Fail", "Change Jobpost Status Success.", "Change Jobpost Status Success.", "Change Jobpost Status API", "data", serializers.errors))
                
            except:
                return Response(getResponseByType("Fail", "Change Jobpost Status Fail.", "Change Candidate Jobpost API", "Change Jobpost Status API", "value", "Change Jobpost Status Fail"))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Change Candidate Status API", "Change Candidate Status API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def request_interview(request):
    if request.data:
        jsondata = eval(request.data["data"])
        
        try:
            request_interview = JobPost.objects.get(id=jsondata["job_id"])
            jsondata["hiring_lead_id"]=request_interview.hiring_lead_id
            serializers = InterviewSerializer(data=jsondata)
            if serializers.is_valid():
                serializers.save()
                try:
                    # Response Detail About Interview
                    get_interview = list(reversed(Interview.objects.filter(candidate_id=jsondata["candidate_id"],job_id=jsondata["job_id"], hiring_lead_id=jsondata["hiring_lead_id"])))
                    
                    # Candid date Detail on candidate_id
                    get_candidate = Candidate.objects.get(id=jsondata["candidate_id"])
                    get_candidate.status = "4"
                    get_candidate.save()
                    # save data after above all condition satisfay
                    
                    serializers = InterviewSerializer(get_interview[0])
                    data = serializers.data
                    data["first_name"]=get_candidate.first_name
                    data["last_name"]=get_candidate.last_name
                    data["contact_no"]=get_candidate.contact_no
                    data["job_title"]=request_interview.job_title
                    data["applied_post_id"]=request_interview.post_id
                    data["fullName"]=get_candidate.first_name+" "+get_candidate.last_name
                    return Response(getResponseByType("Success", "Request Interview Schedule success.", "Request Interview Schedule API", "Request Interview Schedule API", "data", data))

                except Exception as e:
                    return Response(getResponseByType("Fail", "Request Interview Schedule Fail.", "Change Candidate Status API", "Change Candidate Status API", "Value", f"Request Interview Schedule Fail.{e}"))
                
            return Response(getResponseByType("Fail", "Request Interview Schedule Fail.", "Change Candidate Status API", "Change Candidate Status API", "Value", serializers.errors))

        except:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Change Candidate Status API", "Change Candidate Status API", "Value", "insert valid data is reqired, please try again."))

    else:
        return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Change Candidate Status API", "Change Candidate Status API", "Value", "insert valid data is reqired, please try again."))

@api_view(['POST'])
def create_interview_schedule(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            if jsondata["is_created"]=="1":
                try:
                    get_interview_slot = InterviewSlotSchedule.objects.filter(interview_schedule_id=jsondata["interview_id"])
                    get_interview_slot.delete()
                except Exception as e:
                    pass
            
            get_interview = Interview.objects.get(id=jsondata["interview_id"])
            jsondata["status"] = "2"
            serializers = InterviewSerializer(get_interview, data=jsondata, partial=True)
            if serializers.is_valid():
                serializers.save()
                
                for i in range(len(jsondata["interviewTime"])):
                    jsondata["interviewTime"][i]["interview_schedule_id"]=jsondata["interview_id"]
                    serializers=InterviewSlotScheduleSerializer(data=jsondata["interviewTime"][i])
                    if serializers.is_valid():
                        serializers.save()
                
                # Save Email
                get_interview = Interview.objects.get(id=jsondata["interview_id"])
                get_candidate_name = Candidate.objects.get(id=get_interview.candidate_id)
                get_job_title = JobPost.objects.get(id=get_interview.job_id)
                
                get_interview_schedule_template = EmailTemplates.objects.get(name="confirm_interview")
                html = f"{get_interview_schedule_template.template}"
                html = html.replace("first_name", get_candidate_name.first_name).replace("last_name", get_candidate_name.last_name).replace("job_title", get_job_title.job_title).replace("web_link", get_interview.web_link)
                
                obj = Emails()
                obj.from_email = "hello@trukyn.com"
                obj.to_email = get_candidate_name.email
                obj.subject = get_interview_schedule_template.subject
                obj.body = html
                obj.attachment = "File"
                obj.save()
                    

                return Response(getResponseByType("Success", "Create Interview Schedule success.", "Create Interview Schedule API", "Create Interview Schedule API", "value", "Create Interview Schedule success."))

            return Response(getResponseByType("Fail", "Create Interview Schedule Fail.", "Create Interview Schedule API", "Create Interview Schedule API", "Value", serializers.errors))

        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Create Interview Schedule API", "Create Interview Schedule API", "Value", "insert valid data is reqired, please try again."))

@api_view(['POST'])
def change_interview_status(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_interview = Interview.objects.get(id=jsondata["interview_id"])
                get_interview.status =jsondata["status"]
                get_interview.save()
                return Response(getResponseByType("Success", "Change Interview Schedule Status success.", "Change Interview Schedule Status API", "Change Interview Schedule Status API", "value", "Change Interview Schedule success"))

            except:
                return Response(getResponseByType("Fail", "Request Interview Schedule Fail.", "Change Interview Schedule Status API", "Change Interview Schedule Status API", "Value", "Request Interview Schedule Fail."))
    
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Change Interview Schedule Status API", "Change Interview Schedule Status API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def get_interview_by_id(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_interview = Interview.objects.get(id=jsondata["id"], is_deleted="0")
                serializers = InterviewSerializer(get_interview)
                data = serializers.data

                get_job_title = JobPost.objects.get(id = get_interview.job_id)
                data["job_title"]=get_job_title.job_title

                # intreview_status_name() Create Function in Respose.py file
                data["status_name"]=intreview_status_name(get_interview.status)

                # get hiringlead name Find interview table on hiringlead_id
                get_hiringlead_name = User.objects.get(id=get_interview.hiring_lead_id)
                data["hiring_lead_name"]=get_hiringlead_name.first_name+" "+get_hiringlead_name.last_name

                # Interview Sloat schedule finde on interview_schedule_id
                get_interview_slot_schedule_time = InterviewSlotSchedule.objects.filter(interview_schedule_id=get_interview.id)
                serializers = InterviewSlotScheduleSerializer(get_interview_slot_schedule_time, many=True)
                data["interview_slot_schedule_time"]=serializers.data


                return Response(getResponseByType("Success", "Get Interview Scheduled Data found.", "Search Interview Scheduled Data API", "Search Interview Scheduled Data API", "data", data))
            
            except:
                return Response(getResponseByType("Fail", "Get Interview Scheduled Data Fail.", "Search Interview Scheduled Data API", "Search Interview Scheduled Data API", "Value", "Invalid id"))
            
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Search Interview Scheduled Data API", "Search Interview Scheduled Data API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def create_feedback(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                serializers = FeedbackSerializer(data=jsondata)
                if serializers.is_valid():
                    serializers.save()
                    
                    return Response(getResponseByType("Success", "Create FeedBack success.", "Create FeedBack Status API", "Create FeedBack Status API", "value", "Create FeedBack success."))
                
                return Response(getResponseByType("Fail", "Create FeedBack Fail.", "Create FeedBack Status API", "Create FeedBack Status API", "Value", serializers.errors))
            
            except:
                return Response(getResponseByType("Fail", "Create FeedBack Fail, Invalid data.", "Create FeedBack Status API", "Create FeedBack Status API", "Value", "Create FeedBack Fail, Invalid data"))
        
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Create FeedBack Status API", "Create FeedBack Status API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def get_interview_for_candidate(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_interview = Interview.objects.get(id=jsondata["id"], is_deleted="0")
                serializers = InterviewSerializer(get_interview)
                data = serializers.data
                
                get_job_title = JobPost.objects.get(id = get_interview.job_id)
                data["job_title"]=get_job_title.job_title
                
                # intreview_status_name() Create Function in Respose.py file
                data["status_name"]=intreview_status_name(get_interview.status)
                
                # get hiringlead name Find interview table on hiringlead_id
                get_hiringlead_name = User.objects.get(id=get_interview.hiring_lead_id)
                data["hiring_lead_name"]=get_hiringlead_name.first_name+" "+get_hiringlead_name.last_name
                
                data['is_schedule_interview'] = '0'
                
                if data["interview_time"] != None:
                    data['is_schedule_interview'] = '1'

                # Interview Sloat schedule finde on interview_schedule_id 
                try:
                    get_interview_slot_schedule_time = InterviewSlotSchedule.objects.filter(interview_schedule_id=get_interview.id)
                    serializers = InterviewSlotScheduleSerializer(get_interview_slot_schedule_time, many=True)
                    data["interview_slot_schedule_time"]=serializers.data
                except Exception as e:
                    data["interview_slot_schedule_time"]=serializers.data

                # get JobPost Detail Finde Interview Table on Job_id
                serializers = JobPostSerializer(get_job_title)
                data["job_data"]=serializers.data
                
                try:
                    get_candidate_Detail = Candidate.objects.get(id=get_interview.candidate_id)
                    serializers = CandidateSerializer(get_candidate_Detail)
                    data["candidate_data"]=serializers.data
                except Exception as e:
                    data["candidate_data"]=serializers.data

                try:
                    get_offer_data = Offer.objects.get(interview_id=jsondata["id"], status="1")
                    serializers = OfferSerializer(get_offer_data)
                    data["offer_data"]= serializers.data
                except Exception as e:
                    data["offer_data"]= None

                return Response(getResponseByType("Success", "Get Interview Scheduled Data found.", "Search Interview Scheduled Data API", "Search Interview Scheduled Data API", "data", data))
            except:
                return Response(getResponseByType("Fail", "Get Interview Scheduled Data Fail.", "Search Interview Scheduled Data API", "Search Interview Scheduled Data API", "Value", "Invalid id"))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Search Interview Scheduled Data API", "Search Interview Scheduled Data API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def start_interview_process(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                start_Interview = Interview.objects.get(id=jsondata["interview_id"],  is_deleted="0")
                
                if start_Interview.meeting_type == "Web Conference":
                    meeting_id = get_room_id()
                    start_Interview.interview_meeting_id=meeting_id["meetingId"]
                    start_Interview.status= "4"
                    start_Interview.save()

                start_Interview = Interview.objects.get(id=jsondata["interview_id"],  is_deleted="0")
                serializers = InterviewSerializer(start_Interview)
                return Response(getResponseByType("Success", "Start Interview Process success.", "Start Interview Process API", "Start Interview Process API", "data", serializers.data))

            except Exception as e:
                return Response(getResponseByType("Fail", "Fail Interview Process.", "Start Interview Process API", "Start Interview Process API", "Value", f"Invalid interview_id, {e}"))

        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Start Interview Process API", "Start Interview Process API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def get_hiring_lead_interviews(request):
    if request.method == 'POST':
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_interview = list(reversed(Interview.objects.filter(hiring_lead_id=jsondata["hiring_lead_id"], status="3", is_deleted="0")))
                print(get_interview)
                response = []
                if len(get_interview)>0:
                    for i in range(len(get_interview)):
                        if jsondata["start_date"]<get_interview[i].interview_time.strftime("%Y-%m-%d")<jsondata["end_date"]:
                            # get start_time in interview_time sprad
                            end_time = get_interview[i].interview_time + timedelta(minutes=30)

                            response.append({
                                "interview_date":get_interview[i].interview_time.strftime("%Y-%m-%d"),
                                "start_time": get_interview[i].interview_time.strftime("%H:%M:%S"),
                                "end_time": end_time.strftime("%H:%M:%S")
                            })

                return Response(getResponseByType("Success", "Get Interview Scheduled Data found.", "Search Interview Scheduled Data API", "Search Interview Scheduled Data API", "data", response))

            except Exception as e:
                return Response(getResponseByType("Fail", "Invalid request data.", "Get Recruiters Interviews API", "Get Recruiters Interviews API", "Value", f"Recruiter Id Invalid. {e}"))


@api_view(['POST'])
def accept_interview_schedule(request):
    if request.method == 'POST':
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_interview = Interview.objects.get(id=jsondata["interview_id"], is_deleted="0")
                jsondata["status"] = "3"
                serializers = InterviewSerializer(get_interview, data=jsondata, partial=True)
                if serializers.is_valid():
                    serializers.save()
                    
                    # Save Join Email
                    candidate = Candidate.objects.get(id=get_interview.candidate_id)
                    jobDetail = JobPost.objects.get(id=get_interview.job_id)
                    
                    get_schedule_interview = EmailTemplates.objects.get(name="schedule_interview")
                    html = f"{get_schedule_interview.template}"
                    html = html.replace("first_name", candidate.first_name).replace("last_name", candidate.last_name).replace("job_title", jobDetail.job_title).replace("interview_time", get_interview.interview_time.strftime("%A,%B %d, %Y %I:%M %p")).replace("web_link", get_interview.web_link)
                    
                    obj = Emails()
                    obj.from_email = "hello@trukyn.com"
                    obj.to_email = candidate.email
                    obj.subject = get_schedule_interview.subject
                    obj.body = html
                    obj.attachment = "File"
                    obj.save()
                    
                    return Response(getResponseByType("Success", "Accept Interview Schedule success.", "Accept Interview Schedule API", "Accept Interview Schedule API", "value", "Accept Interview Schedule success."))

                return Response(getResponseByType("Fail", "Invalid, please try again.", "Accept Interview Schedule API", "Accept Interview Schedule API", "value", f"Invalid, please try again. {serializers.errors}"))
                    
            except Exception as e:
                return Response(getResponseByType("Fail", "Invalid, please try again.", "Accept Interview Schedule API", "Accept Interview Schedule API", "value", f"Invalid, please try again. {e}"))
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Start Interview Process API", "Start Interview Process API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def offer_candidate(request):
    if request.method == "POST":
        
        if request.data:
            try:
                jsondata = eval(request.data["data"])
                get_interview = Interview.objects.get(id=jsondata["interview_id"])
                data = Candidate.objects.get(id=get_interview.candidate_id)
                job_detail = JobPost.objects.get(id=get_interview.job_id)
                
                # Generate offer Pdf
                context = {
                    'data': data,
                    'job_detail':job_detail,
                    'pay_rate':jsondata["pay_rate"],
                    "pay_rate_type":jsondata["pay_rate_type"],
                    'join_date':jsondata["join_date"],
                    'expiry_date':jsondata["expiry_date"],
                    }
                
                file_name, html = create_pdf(context)
                jsondata["offer_letter_pdf"]="offerletter/"+file_name+".pdf"
                
                serializers = OfferSerializer(data=jsondata)
                if serializers.is_valid():
                    serializers.save()
                    
                    try:
                        # Update Interview details
                        get_interview_data = Interview.objects.get(id=jsondata["interview_id"])
                        get_interview_data.web_link = jsondata["web_link"]
                        get_interview_data.status = "9"
                        get_interview_data.save()
                        
                        # Update candidate details
                        get_candidate = Candidate.objects.get(id=get_interview_data.candidate_id)
                        get_candidate.status = "5"
                        get_candidate.save()
                        
                        # save offer Email
                        get_offer_letter = EmailTemplates.objects.get(name="offer_letter")
                        get_template = f'{get_offer_letter.template}'
                        html = get_template.replace("email_content", jsondata["mail_content"]).replace("web_link", get_interview_data.web_link)
                        pdfname = f'/offerletter/{file_name}.pdf'
                        
                        obj = Emails()
                        obj.from_email = "hello@trukyn.com"
                        obj.to_email = jsondata["offered_email"]
                        obj.subject = jsondata["mail_subject"]
                        obj.body = html
                        obj.attachment = pdfname
                        obj.save()
                        
                        return Response(getResponseByType("Success", "Offer Candidate Success.", "Offer Candidate API", "Offer Candidate API", "value", "Offer Candidate Success."))
                        
                    except Exception as e:
                        return Response(getResponseByType("Fail", "Offer Candidate Fail1.", "Offer Candidate API", "Offer Candidate API", "Value", f"Offer candidate Fail,{e}"))
                        
            except Exception as e:
                return Response(getResponseByType("Fail", "Offer Candidate Fail.", "Offer Candidate API", "Offer Candidate API", "Value", f"Offer candidate Fail,{e}"))

        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Offer Candidate API", "Offer Candidate API", "Value", "insert valid data is reqired, please try again."))


@api_view(['POST'])
def change_offer_status(request):
    if request.method == "POST":
        if request.data:
            jsondata = eval(request.data["data"])
            try:
                get_offer_data = Offer.objects.get(id = jsondata["offer_id"])
                get_offer_data.status = jsondata["status"]
                get_offer_data.save()
                
                if jsondata["status"] == '2':
                    get_interview = Interview.objects.get(id=get_offer_data.interview_id)
                    get_interview.status = "10"
                    get_interview.save()
                    
                    get_candidate = Candidate.objects.get(id=get_interview.candidate_id)
                    get_candidate.status = "6"
                    get_candidate.save()

                return Response(getResponseByType("Success", "Change Offer Status success.", "Change Offer Status API", "Change Offer Status API", "value", "Change Offer success."))
                
            except Exception as e:
                return Response(getResponseByType("Fail", "Change Offer Status Fail.", "Create FeedBack Status API", "Create FeedBack Status API", "Value", "Change Offer Fail."))
                
        else:
            return Response(getResponseByType("Fail", "insert valid data is reqired, please try again.", "Create FeedBack Status API", "Create FeedBack Status API", "Value", "insert valid data is reqired, please try again."))

