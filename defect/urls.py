from django.urls import path

from defect.views import DefectAdd
from device.views import LoginUser, logout_user, ChangePassword

urlpatterns = [
    path('defect_add/<int:pk>/', DefectAdd.as_view(), name='defect_add'),
]
