from django.conf import settings
from django.core.mail import send_mail


def test_send(subject, message, recipients):
	send_mail(
    		subject=subject,
    		message=message,
    		from_email=settings.DEFAULT_FROM_EMAIL,
    		recipient_list=recipients)

def send_email(subject, message, recipients):
	send_mail(
    		subject=subject,
    		message=message,
    		from_email=settings.DEFAULT_FROM_EMAIL,
    		recipient_list=recipients)

def contact_us(message, sender):
	send_mail(
    		subject="Contact Us",
    		message=message,
    		from_email=sender,
    		recipient_list=list(settings.EMAIL_HOST_USER))

def send_email_token(email, token):
	try:
		print("send email")
		subject = 'Welcome to PhysicalAtk'
		message = f'This is your verification code use this to verify your account {str(token)}'
		from_email = settings.DEFAULT_FROM_EMAIL
		recipient_list = [email, ]
		send_mail(subject, message, from_email, recipient_list)
	except Exception as e:
		return False
	
	return True