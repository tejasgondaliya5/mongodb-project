def getResponseByType(type, message, commonTitle="", commonDesc="",responseDataname="data", responseData=""):
    return {
        "status" : type,
        "message": message,
        "Common": {
            "Title": commonTitle,
            "version": "1.0",
            "Description": commonDesc, 
            "Method": "POST"
        },
        "Response": {
            responseDataname: responseData
        }
    }
    

def getResponseByTypewithpagination(type, message, commonTitle="", commonDesc="",responseDataname="data", responseData="", totalrecord="", totalpage="" , currentpage="", parPage=""):
    return {
        "status" : type,
        "message": message,
        "Common": {
            "Title": commonTitle,
            "version": "1.0",
            "Description": commonDesc, 
            "Method": "POST"
        },
        "Response": {
            responseDataname: responseData,
            "totalrecord":totalrecord,
            "totalpage":totalpage,
            "currentpage":currentpage,
            "parPage":parPage
            
        },
        
    }
    
def employment_type(data):
    if data=="0":
        employment_type_name = "Day Shift"
        
    elif data=="1":
        employment_type_name = "Night Shift"
    
    elif data=="2":
        employment_type_name = "Contract"
    
    elif data=="3":
        employment_type_name = "Hourly"
    
    return employment_type_name
        
def minimum_experience(data):
    if data=="0":
        minimum_experience_type = "Entry Level"
    
    elif data=="1":
        minimum_experience_type = "Intermediate"
    
    elif data=="2":
        minimum_experience_type = "Experienced"
    
    return minimum_experience_type

def status_name(type):
    if type=="0":
        status = "Open"
    
    elif type=="1":
        status = "closed"
        
    return status


def intreview_status_name(type):
    if type=="1":
        status = "Pending"
    elif type=="2":
        status = "Waiting"
    elif type=="3":
        status = "Confirmed"
    elif type=="4":
        status = "Processing"
    elif type=="5":
        status = "Completed"
    elif type=="6":
        status = "Rescheduled"
    elif type=="7":
        status = "Rejected"
    elif type=="8":
        status = "Cancelled"
    elif type=="9":
        status = "offered"
    elif type=="10":
        status = "Active(Hired)"
    elif type=="11":
        status = "Deleted"
        
    return status



   