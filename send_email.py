from pymongo import MongoClient
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


client = MongoClient("mongodb+srv://megic:Tejas@cluster0.nakbn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['hyred']
collection = db["hyred_trukyn_emails"]


def send_email():
    all = collection.find({'status':'0'})
    for iteam in all:
        massage = MIMEMultipart()
        massage["To"] = iteam["to_email"]
        massage['Subject'] = iteam["subject"]
        massage.attach(MIMEText(iteam["body"], 'html'))

        if iteam["subject"] != "File":
            try:
                pdf_name = "/var/www/html/hyred-python/media"+iteam["attachment"]
                binary_pdf = open(pdf_name, 'rb')
                payload = MIMEBase('application', 'octate-stream', Name=iteam["attachment"])
                payload.set_payload((binary_pdf).read())
                encoders.encode_base64(payload)
                payload.add_header('Content-Decomposition', 'attachment', filename=iteam["attachment"])
                massage.attach(payload)
            except Exception as e:
                pass
                
        with smtplib.SMTP_SSL("email-smtp.us-west-2.amazonaws.com", 465) as server:
            server.login("AKIAUAWQ7JDE3INTLB2B", "BJRYmL12Gl9UFZrCYNGZ21J0sgw7QdVHHWAYcY3X7IRj")
            text = massage.as_string()
            server.sendmail('support@trukyn.com', iteam["to_email"], text)
            prev = {'status':'0'}
            next = {"$set":{'status':'1'}}
            upd = collection.update_one(prev, next)
            print("mail successfully sent")

send_email()



# try:
#     with open("media/offerletter/offer_letter-fb4f4f3d-ac0e-4cfb-8ffe-ffdc28d5fe22.pdf", 'r') as s:
#         print(s)
# except Exception as e:
#     print(e)





# def send_email():
#     all = collection.find({'status':'0'})
#     for iteam in all:
#         if iteam["subject"] != "This is an Offer letter to Pesley as the Head of Support Manager.":
#             print(iteam["id"])
#             print(iteam["subject"])
#             msg = MIMEText(iteam["body"], 'html')
#             msg['Subject'] = iteam["subject"]
#             msg["To"] = iteam["to_email"]
#             with smtplib.SMTP_SSL("email-smtp.us-west-2.amazonaws.com", 465) as server:
#                 server.login("AKIAUAWQ7JDE3INTLB2B", "BJRYmL12Gl9UFZrCYNGZ21J0sgw7QdVHHWAYcY3X7IRj")
#                 server.sendmail('support@trukyn.com', iteam["to_email"], msg.as_string())
#                 prev = {'status':'0'}
#                 next = {"$set":{'status':'1'}}
#                 upd = collection.update_one(prev, next)
#                 print("mail successfully sent")

# send_email()



