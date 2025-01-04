from .models import TouristDestination
from rest_framework import serializers

class TouristDestinationSerializers(serializers.ModelSerializer):
    class Meta:
        model = TouristDestination  
        fields = '__all__'
