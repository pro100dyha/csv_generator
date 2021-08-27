from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import SchemaFieldFormSet
from .models import DataSchema, DataSet
from celery_tasks.tasks import task_generate_file


class DataSchemaList(generic.ListView):
    queryset = DataSchema.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class DataSchemaFieldCreate(generic.CreateView):
    model = DataSchema
    fields = ['name']
    success_url = reverse_lazy('profile-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['schemafields'] = SchemaFieldFormSet(self.request.POST)
        else:
            data['schemafields'] = SchemaFieldFormSet()
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        schemafields = context['schemafields']
        with transaction.atomic():
            self.object = form.save()

            if schemafields.is_valid():
                schemafields.instance = self.object
                schemafields.save()
        return super().form_valid(form)


class DataSchemaCreate(generic.CreateView):
    model = DataSchema
    fields = ['name']


class DataShemaUpdate(generic.UpdateView):
    model = DataSchema
    success_url = '/'
    fields = ['name']


class DataSchemaFieldUpdate(generic.UpdateView):
    model = DataSchema
    fields = ['name']
    success_url = reverse_lazy('profile-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['schemafields'] = SchemaFieldFormSet(self.request.POST, instance=self.object)
        else:
            data['schemafields'] = SchemaFieldFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        schemafields = context['schemafields']
        with transaction.atomic():
            self.object = form.save()

            if schemafields.is_valid():
                schemafields.instance = self.object
                schemafields.save()
        return super().form_valid(form)


class DataSchemaDelete(generic.DeleteView):
    model = DataSchema
    success_url = reverse_lazy('profile-list')


class DataSetGenerate(generic.ListView):
    model = DataSet
    template_name = 'challenge/datagenerator.html'

    def post(self, request, *args, **kwargs):
        count = request.POST.get('count')
        data_schemas = DataSchema.objects.filter(user=self.request.user)
        for schema in data_schemas:
            data_set, created = DataSet.objects.update_or_create(data_schema=schema, defaults={'count': count})
            if not created:
                data_set.csv_file = None
                data_set.save()
            task_generate_file.delay(data_set.id)
        return redirect('generator')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(data_schema__user=self.request.user)
