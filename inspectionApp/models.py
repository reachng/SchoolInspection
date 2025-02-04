from django.db import models
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=255, blank=True)
    is_inspector = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.school_name:
            self.school_name = "Default School"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.school_name 
        
class Inspection(models.Model):
    school_name = models.CharField(max_length=255)
    sf_code = models.CharField(max_length=100, unique=True)
    inspector_name = models.CharField(max_length=255)
    inspection_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    question_1 = models.CharField(max_length=255,blank=True,null=True,verbose_name="How is the curriculum being implemented, and how does it align with national standards?")
    question_2 = models.CharField(max_length=255,blank=True,null=True,verbose_name="What strategies are in place to ensure student engagement and learning outcomes?")
    question_3 = models.CharField(max_length=255,blank=True,null=True,verbose_name="How do teachers integrate technology into their lessons?")
    question_4 = models.CharField(max_length=255,blank=True,null=True,verbose_name="How is student progress monitored and reported to parents?")
    question_5 = models.CharField(max_length=255,blank=True,null=True,verbose_name="How is discipline maintained in the school?")
    question_6 = models.CharField(max_length=255,blank=True,null=True,verbose_name="Is there a policy in place for emergency situations?")
    question_7 = models.CharField(max_length=255,blank=True,null=True,verbose_name="What strategies are in place to ensure student engagement and learning outcomes?")

    photo = models.ImageField(upload_to='inspection_photos/', blank=True, null=True)

    def __str__(self):
        return f"Inspection for {self.school_name} - {self.inspector_name}"

