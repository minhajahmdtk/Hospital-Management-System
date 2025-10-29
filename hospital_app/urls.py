from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ✅ Patients URLs
    path('view-patients/', views.view_patients, name='view_patients'),
    path('view-patient/<int:patient_id>/', views.view_patient_details, name='view_patient_details'),
    path('delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('patient-home/', views.patient_home, name='patient_home'),
    path('edit-patient/', views.edit_patient, name='edit_patient'),
    path('patient-logout/', views.patient_logout, name='patient_logout'),
    path('take-appointment/', views.take_appointment, name='take_appointment'),
    path('view-appointments/', views.view_appointments, name='view_appointments'),
    path('add-appointments/<int:doctor_id>/', views.add_appointments, name='add_appointments'),
    path('delete-appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    

    # ✅ Medical History
    path('patient_medical_history/', views.patient_medical_history, name='patient_medical_history'),

    # ✅ Doctors
    path('view-doctors/', views.view_doctors, name='view_doctors'),
    path('edit-doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('delete-doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('view-doctor/<int:d_id>/', views.view_doctor_details, name='view_doctor_details'),
    path('view_doctor_detail/<int:doctor_id>/', views.view_doctor_detail, name='view_doctor_detail'),
    

    # ✅ Other pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ✅ Authentication
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('patient-login/', views.patient_login, name='patient_login'),
    path('patient-register/', views.patient_register, name='patient_register'),
    path('doctor-register/', views.doctor_register, name='doctor_register'),
    path('receptionist-login/', views.receptionist_login, name='receptionist_login'),

    # ✅ Receptionist URLs
    path('add_receptionist/', views.add_receptionist, name='add_receptionist'),
    path('view-receptionists/', views.view_receptionists, name='view_receptionists'),
    path('delete-receptionist/<int:r_id>/', views.delete_receptionist, name='delete_receptionist'),
    path('receptionist-home/', views.receptionist_home, name='receptionist_home'),
    path('new-appointments/', views.new_appointments, name='new_appointments'),
    path('assign-status/<int:s_id>/', views.assign_status, name='assign_status'),
    path('confirmed-appointment/', views.confirmed_appointment, name='confirmed_appointment'),
    path('all-appointments/', views.all_appointments, name='all_appointments'),
    path('patient_records/', views.patient_records, name='patient_records'),
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('receptionist-logout/', views.receptionist_logout, name='receptionist_logout'),
    path('add-appointment-receptionist', views.add_appointment_receptionist, name='add_appointment_receptionist'),
    path('view-receptionist/<int:rec_id>/', views.view_receptionist, name='view_receptionist'),

    # ✅ Doctor Page
    path('doctor-home/', views.doctor_home, name='doctor_home'),
    path('appointments-doctor/', views.appointments_doctor, name='appointments_doctor'),
    path('prescription/<int:d_id>/', views.doctor_prescription, name='doctor_prescription'),
    path('view-prescriptions/', views.view_prescriptions, name='view_prescriptions'),
    path('delete_appointment_doctor/<int:app_id>/', views.delete_appointment_doctor, name='delete_appointment_doctor'),
    path('doctor-logout/', views.doctor_logout, name='doctor_logout'),
    path('delete_prescription/<int:pre_id>/', views.delete_prescription, name='delete_prescription'),
   

]
