from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from defect.views import DefectAdd, ApproveAdd, ApproveList, ApproveDelete, ApproveUpdate, ContractorAdd, \
    ContractorList, ContractorDelete, ContractorUpdate, KaitAdd, KaitList, KaitDelete, \
    KaitUpdate, WorkerAdd, WorkerList, WorkerDelete, WorkerUpdate, defect_list, defect_list, DefectUpdate, send_act

urlpatterns = [
    path('defect_add/<int:pk>/', DefectAdd.as_view(), name='defect_add'),
    path('defect_list/', defect_list, name='defect_list'),
    path('defect_update/<int:pk>/', DefectUpdate.as_view(), name='defect_update'),
    path('send_act/<int:pk>/', send_act, name='send_act'),

]
urlpatterns += [path('approve/', ApproveAdd.as_view(), name='approve_add'),
                path('approves/', ApproveList.as_view(), name='approves'),
                # path('approve/<int:pk>', ApproveDetail.as_view(), name='approve_detail'),
                path('approve_delete/<int:pk>/', ApproveDelete.as_view(), name='approve_delete'),
                path('approve_update/<int:pk>/', ApproveUpdate.as_view(), name='approve_update'), ]

urlpatterns += [path('contractor/', ContractorAdd.as_view(), name='contractor_add'),
                path('contractors/', ContractorList.as_view(), name='contractors'),
                # path('contractor/<int:pk>', ContractorDetail.as_view(), name='contractor_detail'),
                path('contractor_delete/<int:pk>/', ContractorDelete.as_view(), name='contractor_delete'),
                path('contractor_update/<int:pk>/', ContractorUpdate.as_view(), name='contractor_update'), ]

urlpatterns += [path('kait/', KaitAdd.as_view(), name='kait_add'),
                path('kaits/', KaitList.as_view(), name='kaits'),
                # path('kait/<int:pk>', KaitDetail.as_view(), name='kait_detail'),
                path('kait_delete/<int:pk>/', KaitDelete.as_view(), name='kait_delete'),
                path('kait_update/<int:pk>/', KaitUpdate.as_view(), name='kait_update'), ]
#
urlpatterns += [path('worker/', WorkerAdd.as_view(), name='worker_add'),
                path('workers/', WorkerList.as_view(), name='workers'),
                # path('worker/<int:pk>', WorkerDetail.as_view(), name='worker_detail'),
                path('worker_delete/<int:pk>/', WorkerDelete.as_view(), name='worker_delete'),
                path('worker_update/<int:pk>/', WorkerUpdate.as_view(), name='worker_update'), ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
