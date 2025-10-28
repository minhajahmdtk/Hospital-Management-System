from django.db import models




# -----------------------
# Doctor Model
# -----------------------


class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    Gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')],default='Male')
    address = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    experience = models.CharField(blank=True, null=True)  # in years     
    qualification = models.CharField(max_length=200, blank=True, null=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




# -----------------------
# Patient Model
# -----------------------
class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    Gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')], default='Male')
    address = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    image = models.ImageField(upload_to='patient_images/', blank=True, null=True)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# -----------------------
# Receptionist Model        
# -----------------------


class Receptionist(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    gender = models.CharField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        default='Male'
    )
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='receptionist_images/', blank=True, null=True)
     
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

# -----------------------
# Appointment Model
# -----------------------       


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    symptoms = models.TextField(max_length=500, null=True, blank=True)
    disease = models.CharField(max_length=200, null=True, blank=True)
    appointment_date = models.DateField(null=True, blank=True)  
    appointment_time=models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )
    

    def __str__(self):
        return f"Appointment: {self.patient} with {self.doctor} ({self.status})"


# -----------------------
# prescription Model
# -----------------------   

class Prescription(models.Model):
    doctor_name = models.CharField(max_length=100, null=True, blank=True)
    patient_name = models.CharField(max_length=100, null=True, blank=True)
    symptoms = models.TextField()
    disease = models.CharField(max_length=200)
    medicines = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.patient_name} by {self.doctor_name}"