#everyclass here represents the table and every attributes defines charfield\datatype

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(max_length=100,unique=True)
    bio=models.TextField(default='no bio...',max_length=300)
    # profile_pic=models.ImageField(null=True,blank=True)
    
    USERNAME_FIELD='email' #this is the field that will be used to login instead of username
    REQUIRED_FIELDS=[] #this is the field that will be required to create a user
 

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

  
class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE,null=True) #this attribute means host value is foreign key that is taken from User Model
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    
    name = models.CharField(max_length=200,null=False)

    description = models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True) #updates time everytimeit is modified
    creadted = models.DateTimeField(auto_now_add=True) #it is taken at first and remains same


    class Meta:
        ordering = ['-updated','-creadted'] #newest at top
    
    def __str__(self):
        return self.name


 
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE) #once room gets deleted all other dat related to it gets deleted,parent delete results in child delete feture of CASCADE
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created= models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-updated','-created'] #newest at top
    
    
    def __str__(self):
        return self.body[0:50]





