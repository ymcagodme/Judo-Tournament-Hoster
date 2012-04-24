from django.db import models
from django.core.files import File
from django.core.files.base import ContentFile

from PyQRNative import *

from cStringIO import StringIO

from IPython import embed


GENDER_CHOICE = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Tournament(models.Model):
    title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logo/', blank=True)

    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name = 'Tournament title'

class Mat(models.Model):
    user = models.ForeignKey('auth.User')
    mat_number = models.CharField(max_length=10)
    def __unicode__(self):
        return "Mat #%s" % (self.mat_number,)

class Division(models.Model):
    mat = models.ForeignKey(Mat, null=True, blank=True)
    match = models.ManyToManyField('Match', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    age = models.CharField(max_length=10, blank=True)
    weight = models.CharField(max_length=10, blank=True)
    rank = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        return "%s %s" % (self.gender.capitalize(), self.age)

class Member(models.Model):
    division = models.ForeignKey(Division, null=True, blank=True)
    user = models.ForeignKey('auth.User')
    SCORE_CHOICE = (
        ('1st', '1st'),        
        ('2nd', '2nd'),        
        ('3rd', '3rd'),        
        ('other', 'Other'),        
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dojo = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    age = models.CharField(max_length=10)
    weight = models.CharField(max_length=10, blank=True)
    place = models.CharField(max_length=10, choices=SCORE_CHOICE, blank=True)
    check_in = models.BooleanField()
    qr_image = models.ImageField(
            upload_to="qr_code/",
            null=True,
            blank=True,
            editable=False
    )

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

def member_pre_save(sender, instance, **kwargs):    
    if not instance.pk:
        instance._QRCODE = True
    else:
        if hasattr(instance, '_QRCODE'):
            instance._QRCODE = False
        else:
            instance._QRCODE = True
models.signals.pre_save.connect(member_pre_save, sender=Member)

def member_post_save(sender, instance, **kwargs):
    if instance._QRCODE:
        instance._QRCODE = False
        if instance.qr_image:
            instance.qr_image.delete()
        qr = QRCode(4, QRErrorCorrectLevel.H)
        qr.addData(str(instance.pk)) # Only accept string
        qr.make()
        image = qr.makeImage()
        ##Save image to string buffer
        image_buffer = StringIO()
        image.save(image_buffer, format='JPEG')
        image_buffer.seek(0)
        ###Here we use django file storage system to save the image.
        file_name = '%s %s.jpg' % (instance.first_name, instance.last_name)
        file_object = File(image_buffer, file_name)
        content_file = ContentFile(file_object.read())
        instance.qr_image.save(file_name, content_file, save=True)
models.signals.post_save.connect(member_post_save, sender=Member)

class Match(models.Model):
    mat = models.ForeignKey(Mat)
    competitors = models.ManyToManyField(Member, null=True, blank=True)
    match_number = models.IntegerField()
    winner = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'matches'

    def __unicode__(self):
        return "Match #%s @ %s" % (self.match_number, self.mat)

#TODO: division_choice / mat_choice ...etc.
