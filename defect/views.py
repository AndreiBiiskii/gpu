from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from rest_framework.reverse import reverse_lazy

from defect.forms import PersonForm
from defect.models import Defect, Approve, Contractor, Kait, Worker
from device.models import Equipment, Position, Location, Status, Description
from device.views import menu


class DefectAdd(CreateView):
    model = Defect
    fields = '__all__'
    success_url = '/'
    template_name = 'defect/defect_add.html'
    extra_context = {
        'title': 'Добавление дефекта',
        'menu': menu,
    }

    def get_initial(self):
        initial = super().get_initial()
        eq = Equipment.objects.get(pk=self.kwargs.get('pk'))
        initial['serial_number'] = eq.serial_number
        initial['defect'] = eq
        initial['gp'] = Position.objects.filter(equipment=eq).last().name
        initial['location'] = Location.objects.filter(equipment=eq).last().name
        initial['status'] = Status.objects.filter(equipment=eq).last().name
        initial['short_description'] = Description.objects.filter(equipment=eq).last().name
        return initial


class ApproveAdd(CreateView):
    model = Approve
    fields = '__all__'
    success_url = reverse_lazy('defect:approves')
    template_name = 'approve/approve_add.html'
    extra_context = {
        'title': 'Добавить подписанта',
        'menu': menu,
    }


class ApproveList(ListView):
    model = Approve
    template_name = 'approve/approve_list.html'
    context_object_name = 'objects'
    extra_context = {
        'title': 'Добавить подписанта',
        'menu': menu,
        'add': 'defect:approve_add',
        'add_delete': 'defect:approve_delete',
        'add_update': 'defect:approve_update'
    }


class ApproveDelete(DeleteView):
    model = Approve
    success_url = reverse_lazy('defect:approves')
    template_name = 'approve/approve_delete.html'
    context_object_name = 'object'
    extra_context = {
        'title': 'Удалить подписанта',
        'menu': menu,
    }


class ApproveUpdate(UpdateView):
    model = Approve
    fields = '__all__'
    success_url = reverse_lazy('defect:approves')
    template_name = 'approve/approve_add.html'
    extra_context = {
        'title': 'Изменить подписанта',
        'menu': menu,
        'add': 'defect:approve_add'
    }


class ContractorAdd(CreateView):
    model = Contractor
    fields = '__all__'
    success_url = reverse_lazy('defect:contractors')
    template_name = 'approve/approve_add.html'
    extra_context = {
        'title': 'Добавить подрядчика',
        'menu': menu,
    }


class ContractorList(ListView):
    model = Contractor
    template_name = 'approve/approve_list.html'
    context_object_name = 'objects'
    extra_context = {
        'title': 'Добавить подрядчика',
        'menu': menu,
        'add': 'defect:contractor_add',
        'add_delete': 'defect:contractor_delete',
        'add_update': 'defect:contractor_update'
    }


class ContractorDelete(DeleteView):
    model = Contractor
    success_url = reverse_lazy('defect:contractors')
    template_name = 'approve/approve_delete.html'
    context_object_name = 'object'
    extra_context = {
        'title': 'Удалить подрядчика',
        'menu': menu,
    }


class ContractorUpdate(UpdateView):
    model = Contractor
    fields = '__all__'
    success_url = reverse_lazy('defect:contractors')
    template_name = 'approve/approve_add.html'
    extra_context = {
        'title': 'Измененить подрядчика',
        'menu': menu,
        'add': 'defect:contractor_add'
    }


class KaitAdd(CreateView):
    model = Kait
    fields = '__all__'
    success_url = reverse_lazy('defect:kaits')
    template_name = 'approve/approve_add.html'
    extra_context = {
        'title': 'Добавить мастера по КАиТ',
        'menu': menu,
    }


class KaitList(ListView):
    model = Kait
    template_name = 'approve/approve_list.html'
    context_object_name = 'objects'
    extra_context = {
        'title': 'Добавить мастера по КАиТ',
        'menu': menu,
        'add': 'defect:kait_add',
        'add_delete': 'defect:kait_delete',
        'add_update': 'defect:kait_update'
    }


class KaitDelete(DeleteView):
    model = Kait
    success_url = reverse_lazy('defect:kaits')
    template_name = 'approve/approve_delete.html'
    context_object_name = 'object'
    extra_context = {
        'title': 'Удалить мастера по КАиТ',
        'menu': menu,
    }


class KaitUpdate(UpdateView):
    model = Kait
    fields = '__all__'
    success_url = reverse_lazy('defect:approves')
    template_name = 'approve/approve_add.html'
    extra_context = {
        'title': 'Изменить мастера по КАиТ',
        'menu': menu,
        'add': 'defect:kait_add'
    }


class WorkerAdd(CreateView):
    model = Worker
    form_class = PersonForm
    fields = '__all__'
    success_url = reverse_lazy('defect:workers')
    template_name = 'approve/approve_add.html'
    extra_context = {
        'title': 'Добавить слесаря',
        'menu': menu,
    }
    success_message = 'Сотрудник успешно добавлен'


class WorkerList(ListView):
    model = Worker
    template_name = 'approve/approve_list.html'
    context_object_name = 'objects'
    extra_context = {
        'title': 'Добавить слесаря',
        'menu': menu,
        'add': 'defect:worker_add',
        'add_delete': 'defect:worker_delete',
        'add_update': 'defect:worker_update'
    }


class WorkerDelete(DeleteView):
    model = Worker
    success_url = reverse_lazy('defect:workers')
    template_name = 'approve/approve_delete.html'
    context_object_name = 'object'
    extra_context = {
        'title': 'Удалить слесаря',
        'menu': menu,
    }


class WorkerUpdate(UpdateView):
    model = Worker
    fields = '__all__'
    success_url = reverse_lazy('defect:workers')
    template_name = 'approve/approve_add.html'
    extra_context = {
        'title': 'Изменить слесаря',
        'menu': menu,
        'add': 'defect:worker_add'
    }
