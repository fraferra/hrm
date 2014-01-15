from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#def create_user_profile(sender, instance, created, **kwargs):
    #if created:
     #   UserProfile.objects.create(user=instance)   

#post_save.connect(create_user_profile, sender=User)

class BusinessUnit(models.Model):
    UNITS = (
      ('Sales', 'Sales'),
      ('Cloud','Cloud'),
      ('SVP-Office', 'SVP-Office'),
     )
    unit=models.CharField(max_length=100, choices= UNITS, null=True)

class UserProfile(models.Model):
    #user=models.ForeignKey(User, unique=True, related_name="")
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length = 20, null=True)
    business_unit=models.ForeignKey(BusinessUnit)

    class Meta:
    	abstract=True

class SeniorVicePresident(UserProfile):
    user=models.OneToOneField(User, unique=True, related_name="seniorvicepresident")
    office=models.CharField(max_length=60, null=True)

class SeniorManager(UserProfile):
    user=models.OneToOneField(User, unique=True, related_name="seniormanager")
    superior = models.ForeignKey(SeniorVicePresident, related_name="subordinates")

class Manager(UserProfile):
    user=models.OneToOneField(User, unique=True, related_name="manager")
    superior = models.ForeignKey(SeniorManager, related_name="subordinates")
    
class Employee(UserProfile):
    user=models.OneToOneField(User, unique=True, related_name="employee")
    SKILL_LEVEL=(
      ('5','5'),
      ('4','4'),
      ('3','3'),
      ('2','2'),
      ('1','1'),

    )
    skill_1=models.CharField(max_length=60, null=True)
    skill_level_1=models.CharField(max_length=30,
                                       choices=SKILL_LEVEL,
                                       default='None', null=True)
    skill_2=models.CharField(max_length=60, null=True)
    skill_level_2=models.CharField(max_length=30,
                                       choices=SKILL_LEVEL,
                                       default='None', null=True)
    skill_3=models.CharField(max_length=60, null=True)
    skill_level_3=models.CharField(max_length=30,
                                       choices=SKILL_LEVEL,
                                       default='None', null=True)
    superior = models.ForeignKey(Manager, related_name="subordinates")





            




