from django.forms import ModelForm, inlineformset_factory
from .models import Agent, Location, Address, AgentReferal, Media
from tagent2.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class AgentForm(ModelForm):
    class Meta:
        model = Agent
        exclude = ()


class LocationForm(ModelForm):
    class Meta:
        model = Location
        exclude = ()


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ()


class AgentReferalForm(ModelForm):
    class Meta:
        model = AgentReferal
        exclude = ()

class MediaForm(ModelForm):
    class Meta:
        model = Media
        exclude = ()



LocationFormSet = inlineformset_factory(Agent, Location, form=LocationForm, extra=1)
AddressFormSet = inlineformset_factory(Agent, Address, form=AddressForm, extra=1)
AgentReferalFormSet = inlineformset_factory(Agent, AgentReferal, form=AgentReferalForm, extra=1)

class SignUpForm(UserCreationForm):
    contact_number = forms.CharField(max_length=20)
    IAM_CHOICES = [
        ('agent', 'AGENT'),
        ('buyer', 'BUYER'),
        ('owner', 'OWNER'),
        ('builder', 'BUILDER'),
    ]

    iam_name = forms.CharField(label='What is your iam choice?', widget=forms.Select(choices=IAM_CHOICES))

    class Meta:
        model = User
        fields = ('username','contact_number','password1', 'password2',)
