from rest_framework import serializers

from .models import Event, Reservation

class EventSeralizer (serializers.ModelSerializer):

    reservations_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'venue', 'date', 'total_seats','available_seats', 
                  'status', 'created_at', 'reservations_count']

    def get_reservations_count (self, object):
        reserved_seats = object.reservations.filter(status = 'confirmed').count()
        return reserved_seats


    def validate(self, data):

        if data.get('available_seats',0)> data.get('total_seats',0):
            raise serializers.ValidationError('Avaialble should should be less than or equal to total seats')
        
        if not data.get('title') :
            raise serializers.ValidationError('Event title is mandatory')

        if not data.get('venue') :
            raise serializers.ValidationError('Event venue is mandatory')

        if not data.get('date') :
                raise serializers.ValidationError('Event date is mandatory')
        
        return data

class ReservationSeralizer(serializers.ModelSerializer):

     class Meta:
        model = Reservation
        fields = ['id', 'event', 'attend_name', 'email','seats_reserved', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

     def validate_seats_reserved(self, data):
            if data < 1:
                raise serializers.ValidationError('Atleat 1 seats should be reserved, negative value or 0 should not be entered')
            return data

     def validate (self, data):
            event = data.get('event')

            if event.status not in ('upcoming', "ongoing"):
                raise serializers.ValidationError (f" you cannot reserve the seats for {event.status} event")
            
            if not data.get ('attend_name'):
                raise serializers.ValidationError ("Event attend name is mandatory")
            
            if not data.get ('email'):
                raise serializers.ValidationError ("email is mandatory")

            if data.get("seats_reserved",0) > event.available_seats:
                raise serializers.ValidationError(f" only {event.available_seats} seats available")

            return data
        
     def create (self, validated_data):
        print (validated_data)
        print("CREATE METHOD CALLED")
        event = validated_data['event']
        event.available_seats -= validated_data['seats_reserved']
        event.save()
        return Reservation.objects.create(** validated_data)