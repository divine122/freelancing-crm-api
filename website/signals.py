from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from user.models import OtpToken  

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
        
            instance.is_active = False
            instance.save(update_fields=['is_active'])  

            # Create OTP
            otp = OtpToken.objects.create(
                user=instance,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
            )

            # Send OTP email
            subject = "Email Verification"
            message = f"""
                Hi {instance.first_name}, here is your OTP: {otp.otp_code}
                It expires in 5 minutes.
                Click the link to verify your email:
                http://127.0.0.1:8000/verify-email/{instance.email}
            """
            sender_email = "d38712653@gmail.com"
            receiver_email = [instance.email]

            send_mail(
                subject,
                message,
                sender_email,
                receiver_email,
                fail_silently=False,
            )
