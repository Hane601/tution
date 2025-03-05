from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Member, student
from django.contrib.auth.views import LoginView
from django.urls import reverse
from twilio.rest import Client
import os
from .models import register, Tutor
from datetime import date
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import json

def home(request):
    if request.method == 'POST':
        masters = Tutor.objects.all()
        username = request.POST.get('username')
        Password = request.POST.get('Password')
        year = request.POST.get('year')
        mahaoya = request.POST.get('Mahaoya', None)
        kakirihena = request.POST.get('Kakirihena', None)
        subject = request.POST.get('subject')
        city = request.POST.get('city')

        for master in masters:
            if master.username == username:
                if check_password(Password, master.password): 
                    messages.success(request, 'You have successfully logged in.')

                    teachers = Tutor.objects.all()
                    for tutors in teachers:
                        if tutors.username == username:
                            if getattr(tutors, subject, False):
                                if getattr(tutors, subject, False):
                                    request.session['sub_id'] = subject
                                    request.session['Year'] = year
                                    request.session['City'] = city

                                    return redirect('Subject_view')
                                else:
                                    messages.error(request, 'Invalid city selection')

                            else:
                                messages.error(request, 'Invalid Subject selection')
                else:
                    messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


@csrf_exempt  # Temporarily disable CSRF for testing
def Subject_view(request):

    if request.method == "POST":
        students = Member.objects.all()
        subject = request.session.get('sub_id', 'No data found')
        Year = request.session.get('Year', 'No data found')
        city = request.session.get('City', 'No data found')
        try:
            data = json.loads(request.body)
            qr_text = data.get("qr_text")

            if not qr_text:
                return JsonResponse({"status": "error", "message": "QR Code text is missing!"}, status=400)

            print(f"Received QR Code: {qr_text}")

            for stus in students:
                print(f"Checking student: {stus.student_id}, QR: {qr_text}")

                if str(stus.student_id).strip() == str(qr_text).strip():
                    if str(stus.year) == str(Year):
                        if getattr(stus, subject, False):
                            if getattr(stus, city, False):
                                account_sid = "AC60fd05ec65cabda215f0550aec371aff"
                                auth_token = "5fe3aecc37896a8aba666a1d3bdfcf44"
                                client = Client(account_sid, auth_token)
                                my_data = f"{subject} {Year} {city}"
                                print(my_data)

                                try: 
                                    register.objects.get(dates=date.today())
                                except register.DoesNotExist:
                                    Register = register(dates=date.today())
                                    Register.save()

                                main_instance = register.objects.get(dates=date.today())  
                                Students = student(
                                    main=main_instance,
                                    student_id=qr_text,
                                    name=stus.firstname,
                                    specific_class=my_data
                                )
                                Students.save()

                                return JsonResponse({"status": "success", "message": "QR Code matched!", "qr_text": qr_text})

            # After checking all students, return an error if no match was found
            return JsonResponse({"status": "error", "message": "No student found!"}, status=400)              

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format!"}, status=400)

    return render(request, 'stus.html')


@login_required
def Message(request):
    members = Member.objects.all()
    account_sid = "AC60fd05ec65cabda215f0550aec371aff"
    auth_token = "5fe3aecc37896a8aba666a1d3bdfcf44"
    client = Client(account_sid, auth_token)
    my_data = request.session.get('subject_year', 'No data found')
    print(my_data)
    if request.method == 'POST':
        ids = request.POST
        present = []
        try: 
            register.objects.get(dates = date.today())
        except:
            Register = register(dates = date.today())
            Register.save()
                
        for value in ids:
            for students in members:
                if students.student_id == value:
                    '''message = client.messages.create(
                    body="Hutto",
                    from_="+15705353619",
                    to="+94773799608",
                    )
                    print(message.body)
                    present.append(students.student_id)'''
                    
                    main_instance = register.objects.get(dates = date.today()) 
                    #print(main_instance)
                    #main_id = main_instance.id
                    Students = student(
                        main = main_instance,
                        student_id = students.student_id,
                        name = students.firstname,
                        specific_class = my_data)

                    Students.save()
                    #now we fucking rendered the phone numbers of the present studends
                    #now write the logic to send the message

        return redirect('home')