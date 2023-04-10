# function based view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Baseapp.models import Room
from .serializers import RoomSerializer


@api_view(['GET']) #user are  only allowed to get data
def getRoutes(request): #this view will show us all routes in api
    routes =[
        'GET /api',
        'GET /api/rooms',  
        'GET /api/room/:id', 
    ]
    return JsonResponse(routes,safe=False) #safe will allow to turn passed python list to json list


@api_view(['GET'])
def getRooms(request):
    rooms=Room.objects.all()
    serialize =RoomSerializer(rooms,many=True) # many mean s there will be many objects
    return Response(serialize.data) #this gonna give us rooms in serialized format

@api_view(['GET'])
def getRoom(request,pk):
    rooms=Room.objects.get(id=pk)
    serializer =RoomSerializer(rooms,many=False) # many mean s there will be many objects
    return Response(serializer.data) #this gonna give us rooms in serialized format

 