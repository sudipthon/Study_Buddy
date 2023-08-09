# from django.contrib.auth.models import User #for importing defualt user model
from django.shortcuts import render, redirect
from django.contrib import (
    messages as messa,
)  # if I import it as messages interpreter will confuse my model Message with built in function messages of just below.
from django.contrib.sites.shortcuts import get_current_site
from .models import (
    Room,
    Topic,
    Message,
    User,
)  # this message model colides with built in messages function
from django.http import HttpResponse
from .forms import RoomForm, MessageForm, UserProfileForm, RegisterForm
from django.db.models import Q  # q lets you have multiple search params
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import (
    login_required,
)  # decorator for adding functionality of user restriction
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
import random

from django.contrib.auth import get_user_model

User = get_user_model()


def generate_code(request):
    num = "12o3pj4qrk5l6n7m890abcdefghi"
    code = ""
    for i in range(6):
        code += random.choice(num)

    request.session['code']=code
    return code


def send_otp(request,recipint, code):
    domain="http://localhost:8000/"
    curren_site = get_current_site(request)
    subject = "Email verification"
    user_email=request.session['email']
    body = render_to_string('mail_template.html', {'code': code, 'domain': domain, 'user': user_email})
    from_= settings.EMAIL_HOST_USER
    to_email=[recipint]

    email=EmailMessage(
        subject,
        body,
        from_,
        to_email,
    )
    email.fail_silently=False

    email.send()




def Log(
    request,
):  # can't name this method login cuase django has login built in function
    page = "login"

    if (
        request.user.is_authenticated
    ):  # if user has already logged in he/she can't go to login page
        return redirect("rooms")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            email = User.objects.get(username=username)
        except:
            return HttpResponse("User doesnot exist")
        user = authenticate(request, username=email, password=password)  # this will either return user object returning these credentials or none

        if user is not None:
           
        
            if user.is_verified:

                login(request, user)  # this object logs in the user with above user variable name storing user name &pass
                return redirect("rooms")
            code=generate_code()
            send_otp(request,user.email, code)
            return HttpResponse("Email is not verified \n Please check your email for verification link")

    context = {"page": page}
    return render(request, "login_register.html", context)


def LogOutUser(request):
    logout(request)
    return redirect("rooms")


def RegisterUser(request):
    form = RegisterForm()
    if request.method == "POST":
        username = request.POST.get("username").lower()
        email = request.POST.get("email").lower()
        request.session['email']=email

        password = request.POST.get("password")

       
        User.objects.create_user(username=username,email=email,password=password)

        code = generate_code(request)
      
        send_otp(request,email, code)
        return render(request,'activation.html',{"user":email})
        
    
    return render(request, "login_register.html", {"form": form})


def main(request):
    return render(request, "Baseapp/mainpage.html")


def verify_email(request,pk):
    email=request.session['email']
    sent_code=request.session['code']
    user=User.objects.get(email=email)
    user_code=pk
    if request.method == "POST":
            user_code=request.POST.get('code')
    if user_code==sent_code:
                user.is_verified=True
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
                return redirect('rooms')





def rooms(request):
    q = (
        request.GET.get("q") if request.GET.get("q") != None else ""
    )  # if there is no argument passed with url it send empty string
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)  # climb up from topic attribute and get to topic model
        | Q(description__icontains=q)
    )
    # 1.when passing no arguments to filter it acts like objects.all and gives all data in list
    # 2.__contains/icontains it will give data even if half od the topic name is matched like python topic even if just 'py' is passed to q
    # 3.Q function lets you have multiple search params by using either and(&) or or(|)

    # rooms=Room.objects.all()  #this gave the list of rooms in database

    room_count = rooms.count()
    topics = Topic.objects.all()[
        0:3
    ]  # [0:5] this will show from ) index to 5 from list of topics
    message = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "messages": message,
    }
    return render(request, "rooms.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)  # get method got the room with specific id
    # messages=room.message_set.all() #<model-name_set_all()> this queries all the child of given specific romm
    messages = (
        room.message_set.all()
    )  # <model-name_set_all()> this queries all the child of given specific romm
    participants = room.participants.all()
    if request.method == "POST":  # to create message
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)  # if someone comments it is added as user
        return redirect("room", pk=room.id)

    context = {"room": room, "messages": messages, "participants": participants}
    return render(request, "room.html", context)


def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = (
        user.room_set.all()
    )  # we can get all the children name by doing specifi obj then model name and underscore set.all
    messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {"user": user, "topics": topics, "rooms": rooms, "messages": messages}
    return render(request, "profile.html", context)


@login_required(
    login_url="login_page"
)  # if user isnot logged in it redirects user to login page else it lets user create room
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(
            name=topic_name
        )  # this will look if existing topic name exists and if it exists it wii ge it else it will create a new one

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        # this will get the topic if it exists if not it will create so get_or_create
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect("rooms")

    context = {"form": form, "topics": topics}
    return render(request, "room_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  # room fields are gonna be prefilled

    if (
        request.user != room.host
    ):  # if room user isnot equal to request user donot allow updating room
        return HttpResponse("You don't have this permission")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        # form = RoomForm(request.POST) #this just adds new room
        # form=RoomForm(request.POST,instance=room) #this tells which room to update
        # if form.is_valid():
        #     form.save()
        return redirect("rooms")

    context = {"form": form, "room": room}
    return render(request, "room_form.html", context)


@login_required(
    login_url="login_page"
)  # if user isnot logged in it redirects user to login page else it lets user delete room
def DeleteRoom(request, pk):
    # this func will renderlast return but when submit button is hit it will satisfy if condition and first return will happen
    room = Room.objects.get(id=pk)

    if (
        request.user != room.host
    ):  # if room user isnot equal to request user donot allow to use this function
        return HttpResponse("You don't have this permission")

    if request.method == "POST":
        room.delete()
        return redirect("rooms")
    return render(request, "delete.html", {"obj": room})


@login_required(
    login_url="login_page"
)  # if user isnot logged in it redirects user to login page else it lets user delete room
def UpdateMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You aren't allowed here!!")
    if request.method == "POST":
        message.delete()
        return redirect("room")
    return render(request, "delete.html", {"obj": message})


@login_required(
    login_url="login_page"
)  # if user isnot logged in it redirects user to login page else it lets user delete room
def DeleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You aren't allowed here!!")

    if request.method == "POST":
        message.delete()
        return redirect("rooms")
    return render(request, "delete.html", {"obj": message})


@login_required(login_url="login")
def UpdateUser(request):
    user = request.user
    form = UserProfileForm(instance=request.user)

    if request.method == "POST":
        user = request.user
        user.bio = request.POST.get("bio")
        if request.FILES.get("profile_pic"):
            user.profile_pic = request.FILES.get("profile_pic")
        user.username = request.POST.get("username")
        user.save()

    return render(request, "update-user.html", {"form": form})


def TopicResponsive(request):
    q = (
        request.GET.get("q") if request.GET.get("q") != None else ""
    )  # if there is no argument passed with url it send empty string

    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "topics_respon.html", {"topics": topics})


def ActivityResponsive(request):
    messages = Message.objects.all()
    return render(request, "activity_respon.html", {"messages": messages})
