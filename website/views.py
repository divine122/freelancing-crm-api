from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm
from .models import Records
from django.contrib.auth import get_user_model
from urllib.parse import unquote, quote
from django.utils import timezone
from user.models import OtpToken
from django.core.mail import send_mail
import random
from datetime import timedelta

# Create your views here.
def home(request):
    records = Records.objects.all()
    #check to see if logging in
    if request.method == "POST" :
        email = request.POST.get('email')
        password = request.POST.get('password')
        #authenticate
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In!')
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
       return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out..")
    return redirect('home')

# def register_user(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()

#             #authenticate login
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password1']
#             user = authenticate(email=email, password=password)
#             login(request, user)
#             messages.success(request, 'You Have Successfully Registered! Welcome...')
#             return redirect('home')
#     else:
#         form = SignUpForm()  
#     return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        #look up record
        customer_record = Records.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, 'You Must Be Logged In To View That Page...')
        return redirect('home')
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Records.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record Deleted Successfully....')
        return redirect('home')
    else:
        messages.success(request, 'You Must Be Logged In To Do That....')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record Added Sucessfully...')
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, 'You Must Be Logged In...')
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Records.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Successfully!...')
            return redirect('home')
        return render(request, 'update_record.html', {
            'form': form,
            'pk': pk
        })
    else:
        messages.success(request, 'You Must Be Logged In...')
        return redirect('home')


def generate_otp():
    return str(random.randint(100000, 999999))


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user until email is verified
            user.save()

            # Generate and save OTP
            otp_code = generate_otp()
            OtpToken.objects.create(
                user=user,
                otp_code=otp_code,
                otp_expires_at=timezone.now() + timedelta(minutes=10)
            )

    

            messages.success(request, "Account Created Successfully! An OTP was sent to your email.")
            return redirect("verify-email", email=user.email)
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form})

def verify_email(request, email):
    email = unquote(email)
    user = get_user_model().objects.get(email=email)
    user_otp = OtpToken.objects.filter(user=user).last()

    if not user_otp:
        messages.error(request, "No OTP found for this account. Please request a new one.")
        return redirect('resend-otp')  # or redirect to a page to resend OTP

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')

        if user_otp.otp_code == otp_code:
            if user_otp.otp_expires_at > timezone.now():  
                user.is_active = True
                user.save()
                messages.success(request, 'Account activated successfully! You can login.')
                return redirect('signin')  
            else:
                messages.warning(request, "The OTP has expired. Get a new OTP!")
                return redirect('verify-email', email=quote(email))
        else:
            messages.warning(request, "Invalid OTP entered. Enter a valid OTP!")
            return redirect('verify-email', email=quote(email))

    return render(request, 'verify_token.html', {'email': email})



def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:    
            login(request, user)
            messages.success(request, f"Hi {request.user.first_name}, you are now logged-in")
            return redirect("home")
        
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
        
    return render(request, "login.html")


def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST.get("otp_email")
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(
                user=user,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
            )

            # URL-encode the email to handle special characters like '+'
            from urllib.parse import quote
            encoded_email = quote(user.email)

            # email variables
            subject = "Email Verification"
            message = f"""
                            Hi {user.first_name}, here is your OTP {otp.otp_code} 
                            It expires in 5 minutes. Use the link below to verify your email:
                            http://127.0.0.1:8000/verify-email/{encoded_email}
                            
                            If you did not request this, you can ignore the message.
                            """
            sender = "d38712653@gmail.com"
            receiver = [user.email, ]

            # send email
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )

            messages.success(request, "A new OTP has been sent to your email address.")
            return redirect("verify-email", email=encoded_email)
        
        else:
            messages.warning(request, "This email doesn't exist in the database.")
            return redirect("resend-otp")

    return render(request, "resend_otp.html")
