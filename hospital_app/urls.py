from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('logout/', views.logout_view, name='logout'),

    # ✅ Patients URLs
    path('view-patients/', views.view_patients, name='view_patients'),
    path('view-patient/<int:patient_id>/', views.view_patient_details, name='view_patient_details'),
    path('delete-patient/<int:id>/', views.delete_patient, name='delete_patient'),
    path('patient-profile/', views.patient_profile, name='patient_profile'),
    path('edit-patient/', views.edit_patient, name='edit_patient'),



    # ✅ Doctors
    path('view-doctors/', views.view_doctors, name='view_doctors'),
    path('edit-doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('delete-doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('view-doctor/<int:d_id>/', views.view_doctor_details, name='view_doctor_details'),

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
]
