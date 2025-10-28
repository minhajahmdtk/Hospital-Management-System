from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Doctor, Patient, Receptionist,Appointment,Prescription
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage





def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


 
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return redirect('admin_home')  
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, 'admin_login.html')


    if not request.user.is_authenticated:
        return redirect('doctor_login')

    try:
        doctor = Doctor.objects.get(email=request.user.email)
    except Doctor.DoesNotExist:
        doctor = None

    total_appointments = Appointment.objects.filter(doctor=doctor).count() if doctor else 0

    return render(request, 'doctor_home.html', {
        'total_appointments': total_appointments,
    })


def admin_home(request):
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    active_doctors = Doctor.objects.filter(is_active=True).count() 
    return render(request, 'admin_home.html', {'total_doctors': total_doctors,
        'total_patients': total_patients,
        'active_doctors': active_doctors,})




def logout_view(request):
    auth.logout(request)
    return redirect('home')



def view_patients(request):
    patients = Patient.objects.all()
    paginator= Paginator(patients, 6)
      
    page_number = request.GET.get('page', 1)
    try:
        patients = paginator.page(page_number)      
    except (InvalidPage, EmptyPage):
        patients = paginator.page(paginator.num_pages)      
    return render(request, 'view_patients.html', {'patients': patients})




def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    return redirect('view_patients')


def view_patient_details(request, patient_id):
    p = get_object_or_404(Patient, id=patient_id)
    return render(request, 'view_patient_details.html', {'patient': p})



def view_doctors(request):
    doctors_list = Doctor.objects.all().order_by('id')
    paginator = Paginator(doctors_list, 6) 

    page_number = request.GET.get('page', 1)
    try:
        doctors = paginator.page(page_number)
    except (InvalidPage, EmptyPage):
        doctors = paginator.page(paginator.num_pages)
    return render(request, 'view_doctors.html', {'doctors': doctors})


def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        status = request.POST.get('status')  
        doctor.is_active = True if status == 'active' else False
        doctor.save()
        messages.success(request, f"{doctor.first_name} {doctor.last_name}'s status updated.")
        return redirect('view_doctors')

    return render(request, 'edit_doctor.html', {'doctor': doctor})


def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    return redirect('view_doctors')

def view_doctor_details(request, d_id):
    d = get_object_or_404(Doctor, id=d_id)
    return render(request, 'view_doctor_details.html', {'doctor': d})


def view_doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'view_doctor_detail.html', {'doctor': doctor})

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('doctor_home') 
        else:
            messages.error(request, "Incorrect username or password!")
            return redirect('doctor_login')
    return render(request, 'doctor_login.html')



def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('patient_home')  
        else:
            messages.error(request, "Incorrect username or password!")
            return redirect('patient_login')
    return render(request, 'patient_login.html')


def patient_home(request):
    if not request.user.is_authenticated:
        return redirect('patient_login')

    try:
       
        patient = Patient.objects.get(email=request.user.email)
    except Patient.DoesNotExist:
        messages.error(request, "Patient profile not found.")
        return redirect('patient_register')

    
    pending_count = Appointment.objects.filter(patient=patient, status='Pending').count()
    confirmed_count = Appointment.objects.filter(patient=patient, status='Confirmed').count()
    cancelled_count = Appointment.objects.filter(patient=patient, status='Cancelled').count()
    completed_count = Appointment.objects.filter(patient=patient, status='Completed').count()

    context = {
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'cancelled_count': cancelled_count,
        'completed_count': completed_count,
    }
    return render(request, 'patient_home.html', context)

def edit_patient(request):
    return render(request, 'edit_patient.html')

def patient_logout(request):
    auth.logout(request)
    return redirect('patient_login')



def take_appointment(request):
    doctors = Doctor.objects.filter(is_active=True).order_by('first_name')  

    paginator = Paginator(doctors, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'take_appointment.html', {'page_obj': page_obj})

def view_appointments(request):
    return render(request, 'view_appointments.html')



def add_appointments(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)

    try:
        patient = Patient.objects.get(email=request.user.email)
    except Patient.DoesNotExist:
        messages.error(request, "No patient profile found with your email. Please register first.")
        return redirect('patient_register')

    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')

        if symptoms:
            
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                symptoms=symptoms,
                status='Pending' 
            )
            messages.success(request, "Appointment request submitted successfully!")
            return redirect('view_appointments')
        else:
            messages.error(request, "Please enter disease and describe your symptoms.")

    return render(request, 'add_appointments.html', {'doctor': doctor})

def view_appointments(request):
    try:
        patient = Patient.objects.get(email=request.user.email)
    except Patient.DoesNotExist:
        messages.error(request, "No patient profile found.")
        return redirect('patient_register')

    appointments_list = Appointment.objects.filter(patient=patient).order_by('-id')

  
    paginator = Paginator(appointments_list, 6) 
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, 'view_appointments.html', {'appointments': appointments})


def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
   
    return redirect('view_appointments')


def patient_medical_history(request):
    if not request.user.is_authenticated:
        return redirect('patient_login')

    patient_name = f"{request.user.first_name} {request.user.last_name}"
    prescriptions = Prescription.objects.filter(patient_name=patient_name).order_by('-id')

    # Pagination setup — 5 records per page
    paginator = Paginator(prescriptions, 5)
    page_number = request.GET.get('page')
    prescriptions_page = paginator.get_page(page_number)

    return render(request, 'patient_medical_history.html', {
        'prescriptions': prescriptions_page
    })



def patient_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['contact']
        gender = request.POST['gender']
        address = request.POST['address']
        blood_group = request.POST['blood_group']
        image = request.FILES.get('image')  

        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('patient_register')

       
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('patient_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists in users")
            return redirect('patient_register')

      
        if Patient.objects.filter(email=email).exists():
            messages.error(request, "Email already exists in patients")
            return redirect('patient_register')

        
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        
        Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            Gender=gender,
            address=address,
            blood_group=blood_group,
            image=image
        )

        return redirect('patient_login')

    return render(request, 'patient_register.html')



def doctor_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['contact']
        gender = request.POST['gender']
        address = request.POST['address']
        image = request.FILES.get('image')
        specialization = request.POST.get('specialization')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')


        if password != confirm_password:
            messages.info(request, "Passwords do not match!")
            return redirect('doctor_register')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists!")
            return redirect('doctor_register')

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists!")
            return redirect('doctor_register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

       
        Doctor.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            Gender=gender,
            address=address,
            specialization=specialization,
            qualification=qualification,
            experience=experience,  
            image=image,
        )

        return redirect('doctor_login')

    return render(request, 'doctor_register.html')



def receptionist_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('receptionist_home')  
        else:
            messages.error(request, "Incorrect username or password!")
            return redirect('receptionist_login')

    return render(request, 'receptionist_login.html')


def add_receptionist(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['contact']
        gender = request.POST['gender']
        address = request.POST['address']
        image = request.FILES.get('image')

        
        if password != confirm_password:
            messages.info(request, "Passwords do not match!")
            return redirect('add_receptionist')

        
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists!")
            return redirect('add_receptionist')

        
        if User.objects.filter(email=email).exists():
            messages.info(request, "Receptionist with this email already exists!")
            return redirect('add_receptionist')

       
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        
        Receptionist.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender,
            address=address,
            image=image
        )

        
        return redirect('admin_home') 

    return render(request, 'add_receptionist.html')

def view_receptionists(request):
    receptionists_list = Receptionist.objects.all().order_by('id')
    paginator = Paginator(receptionists_list, 6)  

    page_number = request.GET.get('page', 1)
    try:
        re = paginator.page(page_number)
    except (InvalidPage, EmptyPage):
        re = paginator.page(paginator.num_pages)

    return render(request, 'view_receptionists.html', {'receptionists': re})



def delete_receptionist(request, r_id):
    receptionist = get_object_or_404(Receptionist, id=r_id)
    receptionist.delete()
    messages.success(request, "Receptionist deleted successfully.")
    return redirect('view_receptionists')


def receptionist_home(request):
   
    new_count = Appointment.objects.filter(status='Pending').count()
    confirmed_count = Appointment.objects.filter(status='Confirmed').count()
    completed_count = Appointment.objects.filter(status='Completed').count()
    cancelled_count = Appointment.objects.filter(status='Cancelled').count()
    total_count = Appointment.objects.all().count()

  
    return render(request, 'receptionist_home.html', {
        'new_appointments': new_count,
        'confirmed_appointments': confirmed_count,
        'total_appointments': total_count,
        'completed_appointments': completed_count,
        'cancelled_appointments': cancelled_count,
    })

def new_appointments(request):
    
    appointments_list = Appointment.objects.all().order_by('appointment_date')

    
    paginator = Paginator(appointments_list, 6)
    page_number = request.GET.get('page')
    appointments = paginator.get_page(page_number)

    return render(request, 'new_appointments.html', {'appointments': appointments})

def assign_status(request, s_id):
    appointment = get_object_or_404(Appointment, id=s_id)

    if request.method == 'POST':
        # Update status
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed', 'Cancelled']:
            appointment.status = new_status
        else:
            messages.error(request, "Invalid status selected.")
            return redirect('assign_status', s_id=s_id)

      
        new_date = request.POST.get('appointment_date')
        if new_date:
            appointment.appointment_date = new_date 

        new_time = request.POST.get('appointment_time')
        if new_time:
            appointment.appointment_time = new_time 

        appointment.save()
        return redirect('new_appointments')

    return render(request, 'assign_status.html', {'appointment': appointment})


def confirmed_appointment(request):
    
    appointments = Appointment.objects.filter(status='Confirmed').order_by('appointment_date')

    #
    paginator = Paginator(appointments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, 'confirmed_appointment.html', {'page_obj': page_obj})

def all_appointments(request):
    appointments = Appointment.objects.all().order_by('-appointment_date')
    
    paginator = Paginator(appointments, 5)
    page_number = request.GET.get('page')
    page_ob = paginator.get_page(page_number)

    return render(request, 'all_appointments.html', {'page_obj': page_ob})

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully.")
    return redirect('all_appointments')

def add_appointment_receptionist(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        patient_id = request.POST.get('patient')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        disease = request.POST.get('disease')
        symptoms = request.POST.get('symptoms')
        status = request.POST.get('status', 'Pending')

        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
        except (Doctor.DoesNotExist, Patient.DoesNotExist):
            messages.error(request, "Invalid Doctor or Patient selected.")
            return redirect('add_appointment')

        
        appointment = Appointment(
            doctor=doctor,
            patient=patient,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            disease=disease,
            symptoms=symptoms,
            status=status
        )
        appointment.save()
        return redirect('all_appointments')  
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    return render(request, 'add_appointment_receptionist.html', {'doctors': doctors, 'patients': patients})

def receptionist_logout (request):
    auth.logout(request)
    return redirect('receptionist_login')





def patient_records(request):
    patients_list = Patient.objects.all()  
    paginator = Paginator(patients_list, 6)
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)
    return render(request, 'patient_records.html', {'patients': patients})
    return redirect('patient_records')

def add_patient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        Gender = request.POST.get('Gender')
        address = request.POST.get('address')
        blood_group = request.POST.get('blood_group')
        image = request.FILES.get('image')

        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            Gender=Gender,
            address=address,
            blood_group=blood_group,
            image=image
        )
        patient.save()
        return redirect('patient_records') 

    return render(request, 'add_patient.html')  

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('patient_records')


def doctor_home(request):
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    try:
        doctor = Doctor.objects.get(email=request.user.email)
    except Doctor.DoesNotExist:
        doctor = None

    total_appointments = Appointment.objects.filter(doctor=doctor).count() if doctor else 0

    return render(request, 'doctor_home.html', {
        'total_appointments': total_appointments,
    })

def appointments_doctor(request):
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    try:
        doctor = Doctor.objects.get(email=request.user.email)
    except Doctor.DoesNotExist:
        messages.error(request, "No appointments found for this doctor.")
        return redirect('doctor_login')

    appointments_list = Appointment.objects.filter(
        doctor=doctor
    ).order_by('-appointment_date', '-appointment_time')

    paginator = Paginator(appointments_list, 6)
    page_number = request.GET.get('page', 1)
    try:
        appointments = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        appointments = paginator.page(paginator.num_pages)

    return render(
        request,
        'appointments_doctor.html',
        {'doctor': doctor, 'appointments': appointments}
    )

def doctor_prescription(request, d_id):
    appointment = get_object_or_404(Appointment, id=d_id)

    if request.method == 'POST':
        patient_name = f"{appointment.patient.first_name} {appointment.patient.last_name}"
        doctor_name = f"{appointment.doctor.first_name} {appointment.doctor.last_name}"
        symptoms = appointment.symptoms
        disease = request.POST.get('disease')
        medicines = request.POST.get('medicines')
        notes = request.POST.get('notes')

        
        pe=Prescription(
            doctor_name=doctor_name,
            patient_name=patient_name,
            symptoms=symptoms,
            disease=disease,
            medicines=medicines,
            notes=notes
        )
        pe.save()
        return redirect('appointments_doctor')

    return render(request, 'doctor_prescription.html', {'appointment': appointment})

def view_prescriptions(request):
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    doctor_name = f"{request.user.first_name} {request.user.last_name}"
    prescriptions_list = Prescription.objects.filter(doctor_name=doctor_name).order_by('-id')

    paginator = Paginator(prescriptions_list, 5)  
    page_number = request.GET.get('page', 1)

    try:
        prescriptions = paginator.page(page_number)
    except (InvalidPage, EmptyPage):
        prescriptions = paginator.page(paginator.num_pages)

    return render(request, 'view_prescriptions.html', {'prescriptions': prescriptions})


def delete_appointment_doctor(request, app_id):
    appointment = get_object_or_404(Appointment, id=app_id)
    appointment.delete()
    return redirect('appointments_doctor')

def delete_prescription(request, pre_id):
    prescription = get_object_or_404(Prescription, id=pre_id)
    prescription.delete()
    return redirect('view_prescriptions')

def doctor_logout(request):
    auth.logout(request)
    
    return redirect('doctor_login')


