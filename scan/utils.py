import qrcode
from django.conf import settings
import logging
from django.template.loader import render_to_string
from django.core.mail import send_mail


logger = logging.getLogger(__name__)

def send_email_with_body(subjet : str, receivers : list, template : str, context : dict):
    try:
        message  = render_to_string(template, context)
        
        send_mail(
            subjet, 
            message,
            settings.EMAIL_HOST_USER,
            fail_silently=True,
            html_message=message
        )
        return True
        
    except Exception as e:
        logger.error()
    return False

def generateQrCode(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    full_name = f"{data['nom']} {data['prenom']} ({data['telephone']}, {data['adresse_mail']})"
    qr.add_data(full_name)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_file = f"{settings.MEDIA_ROOT}/qr_codes/{data['username']}.png"
    img.save(img_file)
    return img_file
