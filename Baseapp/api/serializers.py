from rest_framework.serializers import ModelSerializer
from Baseapp.models import Room


# this a lot looks like form function,serializer converts python objects to json objects

class RoomSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields='__all__' #this will return all the data of room model
