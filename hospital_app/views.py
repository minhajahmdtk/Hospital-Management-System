from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Doctor, Patient, Receptionist,Appointment,Prescription
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage




# -------------------------
# Static pages
# -------------------------
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# -------------------------
# Admin Login
# -------------------------
 
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return redirect('admin_home')  # You can create this page
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, 'admin_login.html')

# -------------------------
# Admin Homedef doctor_home(request):
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
# -------------------------

def admin_home(request):
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    active_doctors = Doctor.objects.filter(is_active=True).count() 
    return render(request, 'admin_home.html', {'total_doctors': total_doctors,
        'total_patients': total_patients,
        'active_doctors': active_doctors,})


# -------------------------
# Admin logout
# -------------------------

def logout_view(request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# -------------------------
# Patient List
# -------------------------

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




# -------------------------
# Doctor List
# -------------------------





def view_doctors(request):
    doctors_list = Doctor.objects.all().order_by('id')
    paginator = Paginator(doctors_list, 6)  # Show 4 doctors per page

    page_number = request.GET.get('page', 1)
    try:
        doctors = paginator.page(page_number)
    except (InvalidPage, EmptyPage):
        doctors = paginator.page(paginator.num_pages)
    return render(request, 'view_doctors.html', {'doctors': doctors})


def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        status = request.POST.get('status')  # Get selected status from form
        doctor.is_active = True if status == 'active' else False
        doctor.save()
        messages.success(request, f"{doctor.first_name} {doctor.last_name}'s status updated.")
        return redirect('view_doctors')

    return render(request, 'edit_doctor.html', {'doctor': doctor})


def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.delete()
    messages.success(request, "Doctor deleted successfully.")
    return redirect('view_doctors')

def view_doctor_details(request, d_id):
    d = get_object_or_404(Doctor, id=d_id)
    return render(request, 'view_doctor_details.html', {'doctor': d})

#-------------------------
# View Doctor Detail  in admin Login      
#-------------------------

def view_doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'view_doctor_detail.html', {'doctor': doctor})
# -------------------------
# Doctor Login
# -------------------------
def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, " logged in successfully!")
            return redirect('doctor_home')  # or a doctor dashboard page
        else:
            messages.error(request, "Incorrect username or password!")
            return redirect('doctor_login')
    return render(request, 'doctor_login.html')


# -------------------------
# Patient Login
# -------------------------
def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "logged in successfully!")
            return redirect('patient_home')  # or a patient dashboard page
        else:
            messages.error(request, "Incorrect username or password!")
            return redirect('patient_login')
    return render(request, 'patient_login.html')


def patient_home(request):
    return render(request, 'patient_home.html')

def edit_patient(request):
    return render(request, 'edit_patient.html')

def patient_logout(request):
    auth.logout(request)
    return redirect('patient_login')

# ---------------- Appintments ----------------

def take_appointment(request):
    doctors = Doctor.objects.filter(is_active=True)  # only show active doctors
    return render(request, 'take_appointment.html', {'doctors': doctors})

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
        disease = request.POST.get('disease')
        symptoms = request.POST.get('symptoms')

        if disease and symptoms:
            # Create appointment with no date yet
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                disease=disease,
                symptoms=symptoms,
                status='Pending'  # date is left as None for receptionist to assign
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

    appointments = Appointment.objects.filter(patient=patient).order_by('-id')  # latest first
    return render(request, 'view_appointments.html', {'appointments': appointments})


def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully.")
    return redirect('view_appointments')
# ---------------- Medical History ----------------

def patient_medical_history(request):
    if not request.user.is_authenticated:
        return redirect('patient_login')

    patient_name = f"{request.user.first_name} {request.user.last_name}"
    prescriptions = Prescription.objects.filter(patient_name=patient_name)

    return render(request, 'patient_medical_history.html', {'prescriptions': prescriptions})


# ---------------- Patient Registration ----------------


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
        image = request.FILES.get('image')  # safer with .get()

        # Password check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('patient_register')

        # Check for existing username/email in User table
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('patient_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists in users")
            return redirect('patient_register')

        # Check for existing email in Patient table
        if Patient.objects.filter(email=email).exists():
            messages.error(request, "Email already exists in patients")
            return redirect('patient_register')

        # Create Django User
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Create Patient record
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

        messages.success(request, "Patient registered successfully. Please login.")
        return redirect('patient_login')

    return render(request, 'patient_register.html')





# ---------------- Doctor Registration ----------------


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

        # Validations
        if len(password) < 6:
            messages.info(request, "Password must be at least 6 characters long!")
            return redirect('doctor_register')

        if password != confirm_password:
            messages.info(request, "Passwords do not match!")
            return redirect('doctor_register')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists!")
            return redirect('doctor_register')

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists!")
            return redirect('doctor_register')

        # Create Django user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create Doctor profile
        Doctor.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            Gender=gender,
            address=address,
            specialization=specialization,
            qualification=qualification,
            experience=experience,  # ✅ added
            image=image,
        )

        messages.success(request, "Doctor registered successfully! Await admin approval.")
        return redirect('doctor_login')

    return render(request, 'doctor_register.html')






# -------------------------
# Receptionist Login (Optional)
# -------------------------
def receptionist_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('receptionist_home')  # replace with your receptionist dashboard
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

        # Password validation
        if password != confirm_password:
            messages.info(request, "Passwords do not match!")
            return redirect('add_receptionist')

        # Check username
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists!")
            return redirect('add_receptionist')

        # Check email
        if User.objects.filter(email=email).exists():
            messages.info(request, "Receptionist with this email already exists!")
            return redirect('add_receptionist')

        # Create user account
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Create receptionist record
        Receptionist.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender,
            address=address,
            image=image
        )

        messages.success(request, "Receptionist added successfully!")
        return redirect('admin_home')  # Redirect to admin home

    return render(request, 'add_receptionist.html')

def view_receptionists(request):
    receptionists_list = Receptionist.objects.all().order_by('id')
    paginator = Paginator(receptionists_list, 6)  # Show 3 receptionists per page

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

#----------receptionist home-----------------   
def receptionist_home(request):
    # Count appointments by status
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
    # Fetch all appointments ordered by date
    appointments = Appointment.objects.all().order_by('appointment_date')
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

        # Update date and time directly from form inputs
        new_date = request.POST.get('appointment_date')
        if new_date:
            appointment.appointment_date = new_date  # Django handles conversion

        new_time = request.POST.get('appointment_time')
        if new_time:
            appointment.appointment_time = new_time  # Django handles conversion

        appointment.save()
        messages.success(request, "Appointment updated successfully.")
        return redirect('new_appointments')

    return render(request, 'assign_status.html', {'appointment': appointment})


def confirmed_appointment(request):
    appointments = Appointment.objects.filter(status='Confirmed').order_by('appointment_date')
    return render(request, 'confirmed_appointment.html', {'appointments': appointments})

def all_appointments(request):
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'all_appointments.html', {'appointments': appointments})

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

        # Fetch related doctor and patient objects
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
        except (Doctor.DoesNotExist, Patient.DoesNotExist):
            messages.error(request, "Invalid Doctor or Patient selected.")
            return redirect('add_appointment')

        # Save appointment
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

        messages.success(request, f"Appointment for {patient.first_name} {patient.last_name} with Dr. {doctor.first_name} added successfully!")
        return redirect('all_appointments')  # Redirect to appointment list

    # GET request: load doctors and patients
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    return render(request, 'add_appointment_receptionist.html', {'doctors': doctors, 'patients': patients})

def receptionist_logout (request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('receptionist_login')



# ---------------- Patient View ----------------

def patient_records(request):
    # Fetch all patients from the database
    patients = Patient.objects.all()
    
    return render(request, 'patient_records.html', {'patients': patients})

def delete_patient_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    messages.success(request, "Patient record deleted successfully.")
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

        # Save patient
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
        return redirect('patient_records')  # redirect to patient list page

    return render(request, 'add_patient.html')           


# ---------------- Doctor Page ----------------

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
    # Check if user is logged in
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    try:
        # Find doctor whose email matches the logged-in user
        doctor = Doctor.objects.get(email=request.user.email)
    except Doctor.DoesNotExist:
        messages.error(request, "No appointments found for this doctor.")
        return redirect('doctor_login')

    # Fetch only that doctor's patients (appointments)
    appointments_list = Appointment.objects.filter(
        doctor=doctor
    ).order_by('-appointment_date', '-appointment_time')

    # ✅ Add pagination (5 per page)
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

        # Save to database
        Prescription.objects.create(
            doctor_name=doctor_name,
            patient_name=patient_name,
            symptoms=symptoms,
            disease=disease,
            medicines=medicines,
            notes=notes
        )

        messages.success(request, "Prescription saved successfully!")
        return redirect('appointments_doctor')

    return render(request, 'doctor_prescription.html', {'appointment': appointment})

def view_prescriptions(request):
    if not request.user.is_authenticated:
        return redirect('doctor_login')

    doctor_name = f"{request.user.first_name} {request.user.last_name}"
    prescriptions_list = Prescription.objects.filter(doctor_name=doctor_name).order_by('-id')

    paginator = Paginator(prescriptions_list, 5)  # Show 5 prescriptions per page
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
    messages.success(request, "Prescription deleted successfully.")
    return redirect('view_prescriptions')

def doctor_logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('doctor_login')


