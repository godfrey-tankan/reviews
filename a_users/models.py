from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True) 
    
    def __str__(self):
        return str(self.user)
    
    @property
    def name(self):
        return self.displayname or self.user.username 
    
    @property
    def avatar(self):
        return self.image.url if self.image else static("images/avatar.svg")

class Individual(models.Model):
    firstname = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    dob = models.DateField()
    position = models.CharField(max_length=255)
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.phone.startswith('07'):
            self.phone = f'263{self.phone[1:]}'

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.firstname} {self.surname}'
    
    def __str__(self):
        return f'{self.firstname} {self.surname}'

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(Individual, related_name='groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def send_message(self, message):
        for _ in self.members.all():
            ...
    def send_notification(self, notification):
        for _ in self.members.all():
            pass