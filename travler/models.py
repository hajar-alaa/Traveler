from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.authtoken.models import Token


class Location(models.Model):
    country = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
#    street = models.CharField(max_length=200, null=False)
    long = models.FloatField(null=False)
    lat = models.FloatField(null=False)
#    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.city


class Activity(models.Model):
    name = models.CharField(max_length=200, null=False)
    details_of_activity = models.TextField(null=False)
    type_of_activity = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=False)
    start_time = models.DateField(_("start at"), null=False)
    end_time = models.DateField(_("end at"), null=False)
    pic = models.ImageField(null=True, blank=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class WorkPlace(models.Model):
    company_name = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=250, null=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    Pro_image = models.ImageField(null=True)
    bio = models.CharField(max_length=500, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    birthDay = models.DateField(_("Birth day"), null=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    facebook = models.URLField(null=True)
    instagram = models.URLField(null=True)
    website = models.URLField(null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    work_place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE, null=True)
    choice_gender = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unspecified', 'Unspecified'),
    )
    gender = models.CharField(
        max_length=32,
        choices=choice_gender, null=True
    )

    def __str__(self):
        return self.first_name


class Visit(models.Model):
    viewer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewer_location = models.ForeignKey(Location, on_delete=models.CASCADE)


#     def __str__(self):
#         return self.viewer_user


class Message(models.Model):
    subject = models.CharField(_("Subject"), max_length=120, blank=True)
    body = models.TextField(_("Body"))
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender_messages',
                               on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver_messages', null=True, blank=True,
                                  on_delete=models.CASCADE)
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)

    def __str__(self):
        return str(self.sender) + " | " + str(self.recipient)
