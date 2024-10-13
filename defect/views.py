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
    def form_valid(self, form):
        form.instance.project = self.request.POST.get('project')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.request.GET.getlist('menu')
        return context
    def get_initial(self):
        initial = super().get_initial()
        initial['defect_act'] = 'kfkfkf'
        return initial



