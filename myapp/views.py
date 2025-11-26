from django.shortcuts import render
from .models import Contact,User
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.

def index(request):
    return render(request, 'index.html')


def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            remarks=request.POST['remarks']
        )
        msg = "Contact saved successfully"
        contact = Contact.objects.all().order_by("-id")[:3]
        return render(request, 'contact.html', {'msg': msg, 'contact': contact})
    else:
        contact = Contact.objects.all().order_by("-id")[:3]
        return render(request, 'contact.html', {'contact': contact})


def signup(request):
    if request.method == "POST":
        try:
            # Check if email is already registered
            User.objects.get(email=request.POST['email'])
            msg = "Email already registered"
            return render(request, 'signup.html', {'msg': msg})

        except:
            # If user doesn't exist, validate password match
            if request.POST['password'] == request.POST['Confirm password']:
                user.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password']
                )
                msg = "User signed up successfully"
                return render(request, 'signup.html', {'msg': msg})
            else:
                msg = "Password and confirm password do not match"
                return render(request, 'signup.html', {'msg': msg})

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method=="POST":
       try:
           user=User.objects.get(email=request.POST['email'])
           if user.password==request.POST['password']:
               request.session['email']=user.email
               request.session['fname']=user.fname
               return render(request,'index.html')

           else:
               msg="Incorrect Password"
               return render(request, 'login.html',{'msg':msg})
       except:
            msg="Email Not Registered"
            return render(request, 'login.html',{'msg':msg})
    else:
        return render(request, 'login.html')

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        msg = "Logged out successfully"
        return render(request, 'login.html', {'msg': msg})
    except:
        msg = "Logged out successfully"
        return render(request, 'login.html', {'msg': msg})

def change_password(request):
    if request.method=="POST":
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                if user.password!=request.POST['new_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    del request.session['email']
                    del request.session['fname']
                    msg="Password Changed Succesfully"
                    return render(request, 'login.html',{'msg':msg})
                else:
                    msg="Your New Password Can't Be From Your Old Password"
                    return render(request,'change-password.html',{'msg':msg})
            else:
                 msg="Your New Password & Confirm New Password Does Not Matched"
                 return render(request,'change-password.html',{'msg':msg})
        else:
             msg="Old Password Does Not Matched"
             return render(request,'change-password.html',{'msg':msg})                
    else:
        return render(request,'change-password.html')
    

def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        user.save()
        msg="Profile Updated Succesfully"
        return render(request,'profile.html',{'user':user,'msg':msg})
    else:
        return render(request,'profile.html',{'user':user})

    
def forgot_password(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            otp = random.randint(1000, 9999)
            context = {}
            address = request.POST['email']
            subject = 'OTP For Forget Password'
            message = 'Hello, your otp for forgot password is ' + str(otp)

            if address and subject and message:
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                    context['result'] = 'Email sent successfully'
                    request.session['otp']=otp
                    request.session['email1']=request.POST['email']
                except Exception as e:
                    context['result'] = f'Error sending email: {e}'
            else:
                context['result'] = 'All fields are required'

            return render(request, "otp.html", context)

        except:
            msg = "Email Not Registered"
            return render(request, 'forgot-password.html', {'msg': msg})

    else:
        return render(request, 'forgot-password.html')

def verify_otp(request):
    otp1=int(request.session['otp'])
    otp2=int(request.POST['otp'])

    if otp1==otp2:
        del request.session['otp']
        return render(request,'new-password.html',{'msg':'Please Set Your New Password'})
    else:
        return render(request,'otp.html',{'msg':'Invalid OTP'})
    
def new_password(request):
    if request.POST['new_password']==request.POST['cnew_password']:
        user=User.objects.get(email=request.session['email1'])
        if user.password!=request.POST['new_password']:
            user.password=request.POST['new_password']
            user.save()
            msg="Password Updated Sussesfully"
            del request.session['email1']
            return render(request,'login.html',{'msg':msg})
        else:
            msg="Your New Password Can't From Your Old Password"
            return render(request,'new-password.html',{'msg':msg})
    else:
        msg="New Password and Confirm New Password Does Not Matched"
        return render(request,'new-password.html',{'msg':msg})