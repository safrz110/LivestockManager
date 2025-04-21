from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    animal_expertise = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(
        unique=True,
        verbose_name='Email Address',
        error_messages={
            'unique': "This email address is already registered.",
        }
    )

    def get_profile_pic_url(self):
        """Get the profile picture URL or return None"""
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        return None

class Owner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)  # Make sure this field exists
    business_name = models.CharField(max_length=100, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class Species(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Species"

class Breed(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='breeds')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['species', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.species.name})"

class Animal(models.Model):
    tag_number = models.CharField(max_length=20, unique=True)
    species = models.CharField(max_length=50)  # Keep this field as is
    breed = models.CharField(max_length=50, blank=True, null=True)  # Keep this field as is
    birth_date = models.DateField()
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.species} - {self.tag_number}"

    def get_age(self):
        """Calculate age in years and months based on birth_date"""
        if not self.birth_date:
            return "Unknown"
        
        today = date.today()
        birth_date = self.birth_date
        
        # Calculate years and months
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        
        # Adjust years and months if needed
        if today.day < birth_date.day:
            months -= 1
        if months < 0:
            years -= 1
            months += 12
            
        # Format age string
        if years == 0:
            if months == 1:
                return f"{months} month"
            return f"{months} months"
        elif years == 1:
            if months == 0:
                return "1 year"
            elif months == 1:
                return f"1 year, 1 month"
            return f"1 year, {months} months"
        else:
            if months == 0:
                return f"{years} years"
            elif months == 1:
                return f"{years} years, 1 month"
            return f"{years} years, {months} months"
    
    def get_age_years(self):
        """Return age in decimal years (for sorting and filtering)"""
        if not self.birth_date:
            return 0
        
        today = date.today()
        birth_date = self.birth_date
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day
        
        # Adjust if birthday hasn't occurred yet this year
        if months < 0 or (months == 0 and days < 0):
            years -= 1
            months += 12
        
        # Add fractional component
        fractional_years = years + (months / 12) + (days / 365.25)
        return round(fractional_years, 1)

class OwnershipTransfer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    ]
    
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE)
    sender = models.ForeignKey('Owner', on_delete=models.CASCADE, related_name='sent_transfers', null=True, blank=True)
    recipient = models.ForeignKey('Owner', on_delete=models.CASCADE, null=True, blank=True, related_name='received_transfers')
    recipient_email = models.EmailField(null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Transfer of {self.animal} from {self.sender} to {self.recipient_email}"
    
    def complete(self, recipient):
        """Complete the transfer process"""
        with transaction.atomic():
            # Update the animal's owner
            self.animal.owner = recipient
            self.animal.save()
            
            # Update transfer status
            self.recipient = recipient
            self.status = 'completed'
            self.completed_date = timezone.now()
            self.save()
    
    def reject(self):
        """Reject the transfer"""
        self.status = 'rejected'
        self.save()
    
    def cancel(self):
        """Cancel the transfer"""
        self.status = 'cancelled'
        self.save()
    
    @property
    def is_outgoing(self):
        """Determine if transfer is outgoing from context perspective"""
        return True  # This will be determined in the template context

class HealthRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('vaccination', 'Vaccination'),
        ('treatment', 'Treatment'),
        ('checkup', 'Regular Checkup'),
        ('other', 'Other')
    ]
    
    # Define all fields with defaults or as nullable to avoid migration issues
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE, related_name='health_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES, default='checkup')
    record_date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=255, default="Health Record")
    description = models.TextField(default="No description provided")
    medications = models.CharField(max_length=255, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    performed_by = models.CharField(max_length=100, blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-record_date']
    
    def __str__(self):
        return f"{self.get_record_type_display()} - {self.animal.tag_number} on {self.record_date}"

class UserPreferences(models.Model):
    """User preferences model"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    browser_notifications = models.BooleanField(default=True)
    default_view = models.CharField(max_length=10, choices=[('table', 'Table'), ('card', 'Card')], default='table')
    language = models.CharField(max_length=5, default='en')
    
    def __str__(self):
        return f"Preferences for {self.user.username}"

class Notification(models.Model):
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        recipient_name = self.recipient.username if self.recipient else "Unknown"
        return f"Notification for {recipient_name}: {self.message[:30]}"

class SupportRequest(models.Model):
    REQUEST_TYPES = [
        ('verification', 'Account Verification'),
        ('activation', 'Account Activation'),
        ('other', 'Other Support')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected')
    ]
    
    username = models.CharField(max_length=150)
    email = models.EmailField()
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_request_type_display()} Request from {self.username} - {self.get_status_display()}"
