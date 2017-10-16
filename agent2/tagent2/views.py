from ajax.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from tagent2.models import Agent
from .forms import *


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'tagent2/agent_list.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'tagent2/agent_list.html')

def model_form_upload(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MediaForm()
    return render(request, 'tagent2/agent_form.html', {
        'form': form
    })


class AgentList(ListView):
    model = Agent

class AgentAddLocArefCreate(CreateView):
    model = Agent
    fields = ['first_name', 'last_name', 'age', 'education', 'company_name', 'specialization', 'experence',
              'agent_notes', 'mobile_number','phone_number', 'email_id', 'media_type', 'image']
    success_url = reverse_lazy('agent-list')

    def get_context_data(self, **kwargs):
        data = super(AgentAddLocArefCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['location'] = LocationFormSet(self.request.POST)
            data['address'] = AddressFormSet(self.request.POST)
            data['agentreferal'] = AgentReferalFormSet(self.request.POST)

        else:
            data['location'] = LocationFormSet()
            data['address'] = AddressFormSet()
            data['agentreferal'] = AgentReferalFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        location = context['location']
        address = context['address']
        agentreferal = context['agentreferal']

        with transaction.atomic():
            self.object = form.save()

            if location.is_valid() and address.is_valid() and agentreferal.is_valid() :
                location.instance = self.object
                address.instance = self.object
                agentreferal.instance = self.object

                location.save()
                address.save()
                agentreferal.save()

        return super(AgentAddLocArefCreate, self).form_valid(form)


class AgentAddLocArefUpdate(UpdateView):
    model = Agent
    fields = ['first_name', 'last_name', 'age', 'education', 'company_name', 'specialization', 'experence',
              'agent_notes', 'mobile_number', 'phone_number', 'email_id', 'media_type', 'image']

    success_url = reverse_lazy('agent-list')

    def get_context_data(self, **kwargs):
        data = super(AgentAddLocArefUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['location'] = LocationFormSet(self.request.POST, instance=self.object)
            data['address'] = AddressFormSet(self.request.POST, instance=self.object)
            data['agentreferal'] = AgentReferalFormSet(self.request.POST, instance=self.object)

        else:
            data['location'] = LocationFormSet(instance=self.object)
            data['address'] = AddressFormSet(instance=self.object)
            data['agentreferal'] = AgentReferalFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        location = context['location']
        address = context['address']
        agentreferal = context['agentreferal']

        with transaction.atomic():
            self.object = form.save()

            if location.is_valid() and address.is_valid() and agentreferal.is_valid():
                location.instance = self.object
                address.instance = self.object
                agentreferal.instance = self.object

                location.save()
                address.save()
                agentreferal.save()

            return super(AgentAddLocArefUpdate, self).form_valid(form)


class AgentDelete(DeleteView):
    model = Agent
    success_url = reverse_lazy('agent-list')

@login_required
def agent_list(request):
    return render(request, 'tagent2/agent_list.html')

def signup(request):
        if request.method == 'POST':
            # text = request.POST['text']
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.profile.contact_number = form.cleaned_data.get('contact_number')
                user.profile.iam_name = form.cleaned_data.get('iam_name')
                username = form.cleaned_data.get('username')
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')

        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


