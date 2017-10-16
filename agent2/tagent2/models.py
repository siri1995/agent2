from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class ContactInfo(models.Model):
    mobile_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    email_id = models.EmailField()


class Media(models.Model):
    media_id = models.AutoField(primary_key=True)
    media_type = models.CharField(max_length=3, blank=True, null=True)
    image = models.ImageField(upload_to='medias/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Agent(ContactInfo, Media):
    agent_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    education = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    experence = models.IntegerField()
    agent_notes = models.TextField()

    def get_absolute_url(self):
        return reverse('agent-update', kwargs={'pk': self.pk})


class Location(models.Model):
    agent = models.ForeignKey(Agent)
    foreign_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=50)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)


class Address(models.Model):
    agent = models.ForeignKey(Agent)
    address_id = models.AutoField(primary_key=True)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    landmark = models.CharField(max_length=20)
    pincode = models.IntegerField()


class AgentReferal(models.Model):
    agent = models.ForeignKey(Agent)
    referal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    verified = models.BooleanField(default=True)


class Profile(models.Model):
    IAM_CHOICES = [
        ('agent', 'AGENT'),
        ('buyer', 'BUYER'),
        ('owner', 'OWNER'),
        ('builder', 'BUILDER'),
    ]
    contact_number = models.CharField(max_length=11)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iam_name = models.CharField(max_length=7)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
