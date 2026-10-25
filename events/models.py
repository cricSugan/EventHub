from django.db import models


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),('ongoing', 'Ongoing'),
        ('completed', 'Completed'),('cancelled', 'Cancelled'),]
    
    title = models.TextField(max_length=200)
    venue = models.TextField(max_length=200)
    date = models.DateField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES, default="upcoming")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.title} at {self.venue}"

    class Meta:
        ordering = ['date']

class Reservation(models.Model):
    STATUS_CHOICES = [('confirmed', 'Confirmed'),
                        ('cancelled', 'Cancelled'),]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name= 'reservations')
    attend_name = models.CharField(max_length=200)
    email = models.EmailField()
    seats_reserved = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return F"{self.attend_name} has reserved the Event {self.event} with {self.seats_reserved}"
    