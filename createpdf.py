from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings
from .models import *


def create_pdf(params:dict):
    template = get_template("offer.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = "offer_letter-"+str(uuid.uuid4())
    print(file_name)
    try:
        with open(str(settings.BASE_DIR)+ f'/media/offerletter/{file_name}.pdf', 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
            
    except Exception as e:
        print(e)
        
    if pdf.err:
        return 'error'
    return file_name, html

