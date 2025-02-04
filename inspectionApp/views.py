from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import InspectorRegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,HttpResponse
from .forms import * 
from django.contrib.auth import authenticate 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
import os
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
import os
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"User {username} logged in successfully.")  # Debugging line
                try:
                    if not user.userprofile.is_inspector:
                        print("User is not an inspector.")  # Debugging line
                except UserProfile.DoesNotExist:
                    print("User profile does not exist.")  # Debugging line
                return redirect('inspection_form')
            else:
                print("Authentication failed.")  # Debugging line
                return redirect('login')  # Redirect back to login if authentication fails
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

import csv
from inspectionApp.models import Inspection

def migrate_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Map CSV fields to Inspection model fields
            inspection = Inspection(
                sf_code=row['SF Code'],
                school_name=row['School Name'],
                inspector_name=row['Inspector Name'],
                inspection_date=row['Inspection Date'],
                # Add more fields as necessary
            )
            inspection.save()

# Call the function with your CSV file path
#migrate_data_from_csv('/home/webapp/SchoolInspect/templates/jotform_data.csv')

@login_required
def inspection_form_view(request):
    try:
        if not request.user.userprofile.is_inspector:
            return redirect('login')  # User is not an inspector, redirect to login
    except UserProfile.DoesNotExist:
        return redirect('create_userprofile')  # User doesn't have a profile, redirect to create it

    # Continue with form logic
    sf_code = request.GET.get('sf_code', None)
    form = InspectionForm()
    previous_inspection = None

    if sf_code:
        try:
            previous_inspection = Inspection.objects.filter(sf_code=sf_code).latest('inspection_date')
            form = InspectionForm(instance=previous_inspection)
        except Inspection.DoesNotExist:
            form = InspectionForm(initial={'sf_code': sf_code})

    if request.method == 'POST':
        if previous_inspection:
            form = InspectionForm(request.POST, request.FILES, instance=previous_inspection)
        else:
            form = InspectionForm(request.POST, request.FILES)

        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.completed = 'completed' in request.POST
            inspection.save()
            return redirect('inspection_form')

    return render(request, 'inspection_form.html', {'form': form, 'sf_code': sf_code})


from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
import os

@login_required
def inspection_step(request, step=1):
    # Restrict step to a maximum of 2 (two steps total)
    if step > 2:
        return redirect('inspection_complete')

    # Handle form initialization for GET or POST
    if request.method == "POST":
        # Retrieve or initialize form
        if 'inspection_id' in request.session:
            try:
                inspection = Inspection.objects.get(id=request.session['inspection_id'])
                form = InspectionForm(request.POST, request.FILES, instance=inspection)
            except Inspection.DoesNotExist:
                form = InspectionForm(request.POST, request.FILES)
        else:
            form = InspectionForm(request.POST, request.FILES)

        if form.is_valid():
            inspection = form.save(commit=False)
            # Save the inspection and store ID in session
            inspection.save()
            request.session['inspection_id'] = inspection.id

            # If on step 2, check for 'complete' and finalize
            if step == 2:
                if 'complete' in request.POST:
                    inspection.completed = True
                    inspection.save()

                    # Generate PDF
                    pdf_path = generate_pdf(inspection)

                    # Send email with PDF attached
                    send_inspection_email(inspection, pdf_path)

                    # Clear session
                    del request.session['inspection_id']
                    return redirect('inspection_complete')

            # Proceed to the next step
            return redirect('inspection_step', step=step + 1)

    else:
        # Handle form initialization for GET (initial load)
        if 'inspection_id' in request.session:
            try:
                inspection = Inspection.objects.get(id=request.session['inspection_id'])
                form = InspectionForm(instance=inspection)
            except Inspection.DoesNotExist:
                form = InspectionForm()
                del request.session['inspection_id']
        else:
            form = InspectionForm()

    # Adjust form context based on the step
    context = {
        'form': form,
        'step': step,
    }

    return render(request, 'inspection_step.html', context)


def generate_pdf(inspection):
    # Define the file path
    pdf_directory = '/home/webapp/SchoolInspect/PDFs'
    os.makedirs(pdf_directory, exist_ok=True)
    file_path = os.path.join(pdf_directory, f'inspection_{inspection.sf_code}.pdf')

    # Create a PDF and save it to the specified path
    p = canvas.Canvas(file_path)
    p.drawString(100, 800, f"Inspection Report for {inspection.school_name}")
    p.drawString(100, 780, f"SF Code: {inspection.sf_code}")
    p.drawString(100, 760, f"Inspector: {inspection.inspector_name}")
    p.drawString(100, 740, f"Date: {inspection.inspection_date}")

    # Add more fields as needed
    p.showPage()
    p.save()

    return file_path

def send_inspection_email(inspection, pdf_path):
    email = EmailMessage(
        subject=f"Inspection Report for {inspection.school_name}",
        body=f"Dear {inspection.inspector_name},\n\nPlease find the attached inspection report for {inspection.school_name} (SF Code: {inspection.sf_code}).\n\nBest regards,\nInspection Team",
        from_email='businessintelligencemcm@gmail.com',
        to=['bideptartment8976@gmail.com'],  # Send to the specified email address
    )
    
    # Attach the PDF
    email.attach_file(pdf_path)
    
    # Send the email
    email.send()


@login_required
def inspection_complete(request):
    # Check if the user is allowed to access this page
    if not request.session.get('form_submitted', False):
        # Redirect to the inspection form if not submitted
        messages.info(request, "You must complete the form first.")
        return redirect('inspection_form')
    
    # Clear the session variable after rendering the success page
    request.session['form_submitted'] = False
    return render(request, 'inspection_complete.html')
    

@csrf_exempt
@login_required
def autosave_inspection(request):
    if request.method == 'POST':
        form = InspectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    


                                        