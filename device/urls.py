from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .parser import data_from_parser, save_file
from .sending import sending, send_all
from .views import *

urlpatterns = [
    path('', equipment_list, name='search'),
    path('changes', changes, name='changes'),
    path('send_all/<int:start>/<int:end>', send_all, name='send_all'),
    path('send/<slug:title>', sending, name='send'),
    path('my_exams', my_exams, name='my_exams'),
    # path('data_from_parser/', data_from_parser, name='data_from_parser'),
    path('data_from_parser/', save_file, name='data_from_parser'),


    path('users/', include(('users.urls', 'users'), namespace='users')),
    # path('defects/', include(('defectone.urls', 'defectone'), namespace='defectone')),
    path('draft', DraftCreate.as_view(), name='draft'),
    path('draft_list/', DraftList.as_view(), name='draft_list'),
    path('draft_detail/<int:pk>', DraftDetail.as_view(), name='draft_detail'),
    path('draft_equipment_add/<int:pk>', draft_equipment_add, name='draft_equipment_add'),
    path('draft_device_add/<int:pk>', draft_device_add, name='draft_device_add'),
    path('draft_delete/<int:pk>', draft_delete, name='draft_delete'),
    path('equipment_add/', equipment_add, name='equipment_add'),
    path('equipment_detail/<int:pk>', equipment_detail, name='equipment_detail'),
    path('equipment_update/<int:pk>', EquipmentUpdate, name='equipment_update'),
    path('equipment_delete/<int:pk>', EquipmentDelete, name='equipment_delete'),
    path('device_add/', device_add, name='device_add'),
    path('device_update/<int:pk>', DeviceUpdate, name='device_update'),
    path('send_bid/<int:pk>/', send_bid, name='send_bid'),
    path('ppr_date_add/', PprDateCreate.as_view(), name='ppr_date_add'),
    path('ppr_date_update/<int:pk>/', PprDateUpdate.as_view(), name='ppr_date_update'),
    path('ppr_date_list/', PprDateList.as_view(), name='ppr_date_list'),
    path('ppr_list/<int:pk>/', get_ppr_list, name='ppr_list'),
    # path('ppr_list/', PprList.as_view(), name='ppr_list'),
    path('ppr_add/<int:pk>/', ppr_create, name='ppr_add'),
    # path('ppr_detail/<int:pk>', PprDetail.as_view(), name='ppr_detail'),
    path('ppr_update/<int:pk>', PprUpdate.as_view(), name='ppr_update'),
    # path('ppr_delete/<int:pk>', PprDelete.as_view(), name='ppr_delete'),
    # path('im/', IM, name='im'),
    # path('si_loading/<int:i>', si_loading, name='si_loading'),
    path('manuals/', ManualsView.as_view(), name='manuals'),
    path('manufacturers/', ListCategory.as_view(model=Manufacturer, extra_context={
        'title': 'Список производителей',
        'menu': menu,
        'url_delete': 'delete_manufacturer',
        'url_update': 'update_manufacturer',
        'url_add': 'add_manufacturer'
    }), name='manufacturers'),
    # path('delete_manufacturer/<int:pk>', delete_category, {'Mod': Manufacturer}, name='delete_manufacturer'),
    path('add_manufacturer/', AddCategory.as_view(model=Manufacturer), name='add_manufacturer'),
    path('update_manufacturer/<int:pk>', UpdateCategory.as_view(model=Manufacturer), name='update_manufacturer'),
    path('models/', ListModel.as_view(), name='models'),
    # path('delete_model/<int:pk>', delete_category, {'Mod': EquipmentModel}, name='delete_model'),
    path('add_model/', AddCategory.as_view(model=EquipmentModel), name='add_model'),
    path('update_model/<int:pk>', UpdateCategory.as_view(model=EquipmentModel), name='update_model'),
    # path('types/', ListCategory.as_view(model=EquipmentType, extra_context={
    #     'title': 'Список типов',
    #     'menu': menu,
    #     'url_delete': 'delete_type',
    #     'url_update': 'update_type',
    #     'url_add': 'add_type'
    # }), name='types'),
    # # path('delete_type/<int:pk>', delete_category, {'Mod': EquipmentType}, name='delete_type'),
    # path('add_type/', AddCategory.as_view(model=EquipmentType), name='add_type'),
    # path('update_type/<int:pk>', UpdateCategory.as_view(model=EquipmentType), name='update_type'),

    path('names/', ListCategory.as_view(model=EquipmentName, extra_context={
        'title': 'Наименование оборудования',
        'menu': menu,
        'url_delete': 'delete_name',
        'url_update': 'update_name',
        'url_add': 'add_name'
    }), name='names'),
    # path('delete_name/<int:pk>', delete_category, {'Mod': EquipmentName}, name='delete_name'),
    path('add_name/', AddCategory.as_view(model=EquipmentName), name='add_name'),
    path('update_name/<int:pk>', UpdateCategory.as_view(model=EquipmentName), name='update_name'),

    path('statuses/', ListCategory.as_view(model=StatusAdd, extra_context={
        'title': 'Статус',
        'menu': menu,
        'url_delete': 'delete_status',
        'url_update': 'update_status',
        'url_add': 'add_status'
    }), name='statuses'),
    # path('delete_status/<int:pk>', delete_category, {'Mod': StatusAdd}, name='delete_status'),
    path('add_status/', AddCategory.as_view(model=StatusAdd), name='add_status'),
    path('update_status/<int:pk>', UpdateCategory.as_view(model=StatusAdd), name='update_status'),

    path('list_gp/', ListGP.as_view(), name='list_gp'),
    path('delete_gp/<int:pk>', delete_gp, name='delete_gp'),
    path('add_gp/', AddGp.as_view(), name='add_gp'),
    path('update_gp/<int:pk>', UpdateGp.as_view(), name='update_gp'),

    path('years/', ListCategory.as_view(model=Year, extra_context={
        'title': 'Год выпуска.',
        'menu': menu,
        'url_delete': 'delete_year',
        'url_update': 'update_year',
        'url_add': 'add_year'
    }), name='years'),
    # path('delete_year/<int:pk>', delete_category, {'Mod': Year}, name='delete_year'),
    path('add_year/', AddCategory.as_view(model=Year), name='add_year'),
    path('update_year/<int:pk>', UpdateCategory.as_view(model=Year), name='update_year'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
