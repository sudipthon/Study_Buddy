from django .forms import ModelForm
from .models import Room,Message,User
from django.contrib.auth.models import User #for importing user model

from django.contrib.auth import get_user_model
User = get_user_model()
class RoomForm(ModelForm):
    class Meta:
        model = Room #the model for which form is being created
        fields = '__all__' # input fields will be created for all attribute of input of Room model of rooms.py
        exclude= ['host','participants']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields= '__all__'

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields= ['username','email','password']

class UserProfileForm(ModelForm):
    class Meta:
        model=User
        fields=['username','bio','profile_pic']
   

