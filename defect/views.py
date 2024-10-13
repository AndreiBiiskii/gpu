from django.shortcuts import render, redirect
from django.views.generic import CreateView

from defect.models import Defect


class DefectAdd(CreateView):
    model = Defect
    fields = '__all__'
    success_url = '/'
    template_name = 'defect/defect_add.html'
    extra_context = {
        'title': 'Добавление дефекта',
    }

    def get_initial(self):
        initial = super().get_initial()
        initial['defect_act'] = 'kfkfkf'
        return initial
