from django.db import models

GENDER_CHOICE = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class Mat(models.Model):
    mat_number = models.CharField(max_length=10)
    def __unicode__(self):
        return "Mat #%s" % (self.mat_number,)

class Division(models.Model):
    mat = models.ForeignKey(Mat, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    age = models.CharField(max_length=10, blank=True)
    weight = models.CharField(max_length=10, blank=True)
    rank = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        return "%s %s" % (self.gender.capitalize(), self.age)

class Member(models.Model):
    division = models.ForeignKey(Division, null=True, blank=True)
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
    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Match(models.Model):

    competitors = models.ManyToManyField(Member, null=True, blank=True)
    match_number = models.IntegerField()
    winner = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "Match #%s" % (self.match_number, )

#TODO: division_choice / mat_choice ...etc.