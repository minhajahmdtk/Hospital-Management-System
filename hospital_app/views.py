from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Doctor, Patient, Receptionist,Appointment
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
        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return redirect('admin_home')  # You can create this page
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, 'admin_login.html')

# -------------------------
# Admin Home
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
    return render(request, 'view_patients.html', {'patients': patients})




def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    messages.success(request, "Patient deleted successfully.")
    return redirect('view_patients')


def view_patient_details(request, patient_id):
    p = get_object_or_404(Patient, id=patient_id)
    return render(request, 'view_patient_details.html', {'patient': p})




# -------------------------
# Doctor List
# -------------------------





def view_doctors(request):
    doctors_list = Doctor.objects.all().order_by('id')
    paginator = Paginator(doctors_list, 4)  # Show 4 doctors per page

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
            return redirect('home')  # or a doctor dashboard page
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
    messages.success(request, "You have been logged out.")
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
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                disease=disease,
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

    appointments = Appointment.objects.filter(patient=patient).order_by('-id')  # latest first
    return render(request, 'view_appointments.html', {'appointments': appointments})


def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully.")
    return redirect('view_appointments')
# ---------------- Medical History ----------------

def medical_history(request):
    return render(request, 'view_medical_history.html')


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

        if password != confirm_password:
            messages.info(request, "Passwords do not match!")
            return redirect('doctor_register')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists!")
            return redirect('doctor_register')

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists!")
            return redirect('doctor_register')

        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        user.save()

        Doctor.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            Gender=gender,
            address=address,
            image=image,
        )

        messages.success(request, "Doctor registered successfully!")
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
    re = Receptionist.objects.all()
    return render(request, 'view_receptionists.html', {'receptionists': re})



def delete_receptionist(request, r_id):
    receptionist = get_object_or_404(Receptionist, id=r_id)
    receptionist.delete()
    messages.success(request, "Receptionist deleted successfully.")
    return redirect('view_receptionists')

#----------receptionist home-----------------   
def receptionist_home(request):
    return render(request, 'receptionist_home.html')