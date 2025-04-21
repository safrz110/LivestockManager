from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, models
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt, csrf_protect
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q, Count
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.core.paginator import Paginator
import random
import string
import json
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta
from .forms import CustomUserCreationForm, AnimalForm
from .models import Animal, Owner, Species, Breed, CustomUser, OwnershipTransfer, HealthRecord, SupportRequest, Notification

# Home view
def home(request):
    return render(request, 'home.html')

# Login view
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

# Logout view
def custom_logout(request):
    logout(request)
    return redirect('home')

# Register view
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    # Additional email validation
                    if CustomUser.objects.filter(email=user.email).exists():
                        messages.error(request, 'A user with this email already exists.')
                        return render(request, 'registration/register.html', {'form': form})
                    user.save()
                    messages.success(request, 'Registration successful! Please login.')
                    return redirect('login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def animal_list(request):
    """View for listing animals"""
    try:
        user_owner = Owner.objects.get(user=request.user)
        animals = Animal.objects.filter(owner=user_owner)
        
        # Get all species and breeds
        all_species = Species.objects.all().order_by('name')
        all_breeds = Breed.objects.all().order_by('name')
        
        search_query = request.GET.get('search', '')
        species_filter = request.GET.get('species', '')
        sex_filter = request.GET.get('sex', '')
        
        if search_query:
            animals = animals.filter(
                Q(tag_number__icontains=search_query) |
                Q(species__name__icontains=search_query) |
                Q(breed__name__icontains=search_query)
            )
        
        if species_filter:
            animals = animals.filter(species__name=species_filter)
            
        if sex_filter:
            animals = animals.filter(sex=sex_filter)
        
        context = {
            'animals': animals,
            'total_count': animals.count(),
            'all_species': all_species,
            'all_breeds': all_breeds,
            'search_query': search_query,
            'species_filter': species_filter,
            'sex_filter': sex_filter,
            'species_count': all_species.count(),
            'male_count': animals.filter(sex='Male').count(),
            'female_count': animals.filter(sex='Female').count()
        }
    except Owner.DoesNotExist:
        user_owner = Owner.objects.create(user=request.user)
        context = {
            'animals': [],
            'total_count': 0,
            'all_species': [],
            'all_breeds': [],
            'search_query': '',
            'species_filter': '',
            'sex_filter': '',
            'species_count': 0,
            'male_count': 0,
            'female_count': 0
        }
    
    return render(request, 'animal_list.html', context)

# Add new API endpoint to get breeds by species
@login_required
def get_breeds_by_species(request):
    species_id = request.GET.get('species_id')
    if species_id:
        breeds = Breed.objects.filter(species_id=species_id).values('id', 'name')
        return JsonResponse(list(breeds), safe=False)
    return JsonResponse([], safe=False)

@login_required
def add_animal(request):
    all_species = Species.objects.all().order_by('name')
    
    if request.method == 'POST':
        form = AnimalForm(request.POST, user=request.user)
        if form.is_valid():
            animal = form.save(commit=False)
            owner = Owner.objects.get_or_create(user=request.user)[0]
            animal.owner = owner
            animal.save()
            messages.success(request, 'Animal added successfully!')
            return redirect('animal_list')
    else:
        form = AnimalForm(user=request.user)
    
    context = {
        'species_list': all_species,
        'form': form
    }
    return render(request, 'add_animal.html', context)

# Add a new view for getting breeds by species
@login_required
def get_breeds_for_species(request):
    species_id = request.GET.get('species_id')
    if species_id:
        breeds = Breed.objects.filter(species_id=species_id).values('id', 'name')
        return JsonResponse(list(breeds), safe=False)
    return JsonResponse([], safe=False)

# Generate tag API
def generate_tag(request):
    """Generate a unique animal tag number"""
    # Create a more robust tag generation system
    prefix = "LV"
    # Generate a random 5-digit number
    random_digits = ''.join(random.choices(string.digits, k=5))
    # Format: LV-XXXXX (e.g., LV-12345)
    tag_number = f"{prefix}-{random_digits}"
    
    # Check if this tag already exists, if so, generate a new one
    while Animal.objects.filter(tag_number=tag_number).exists():
        random_digits = ''.join(random.choices(string.digits, k=5))
        tag_number = f"{prefix}-{random_digits}"
    
    return JsonResponse({'tag': tag_number, 'success': True})

@login_required
def find_user(request):
    """API to find a user for ownership transfer"""
    if request.method == 'GET':
        identifier = request.GET.get('identifier', '').strip()
        if not identifier:
            return JsonResponse({'found': False, 'error': 'No username or email provided'})
        
        # Don't allow transferring to yourself
        if (request.user.username.lower() == identifier.lower() or 
            request.user.email.lower() == identifier.lower()):
            return JsonResponse({'found': False, 'error': 'Cannot transfer to yourself'})
        
        try:
            # Look for user by username or email
            user = CustomUser.objects.get(
                Q(username__iexact=identifier) | Q(email__iexact=identifier)
            )
            
            # Try to get or create owner for the user
            owner, created = Owner.objects.get_or_create(user=user)
            
            return JsonResponse({
                'found': True,
                'id': owner.id,
                'user_id': user.id,
                'username': user.username,
                'name': user.get_full_name(),
                'email': user.email,
                'profile_pic': user.profile_pic.url if hasattr(user, 'profile_pic') and user.profile_pic else None,
                'is_verified': getattr(user, 'is_verified', False)
            })
        except CustomUser.DoesNotExist:
            return JsonResponse({'found': False, 'error': 'User not found'})
        except Exception as e:
            return JsonResponse({'found': False, 'error': str(e)})
    
    return JsonResponse({'found': False, 'error': 'Invalid request method'})

# Profile view
def profile(request):
    return render(request, 'profile/profile.html')

# Change password view
def change_password(request):
    return render(request, 'profile/password.html')

# Update preferences view
def update_preferences(request):
    return render(request, 'profile/preferences.html')

@login_required
def ownership(request):
    """View for managing animal ownership and transfers"""
    try:
        user_owner = Owner.objects.get(user=request.user)
        animals = Animal.objects.filter(owner=user_owner)
        
        # Get pending transfers initiated by the user
        pending_transfers = OwnershipTransfer.objects.filter(
            sender=user_owner,
            status='pending'
        ).order_by('-created_at')
        
        # Get incoming transfer requests
        incoming_transfers = OwnershipTransfer.objects.filter(
            recipient=user_owner,
            status='pending'
        ).order_by('-created_at')
        
        # Get transfer history
        transfer_history = OwnershipTransfer.objects.filter(
            Q(sender=user_owner) | Q(recipient=user_owner)
        ).exclude(status='pending').order_by('-created_at')
        
        context = {
            'animals': animals,
            'pending_transfers': pending_transfers,
            'incoming_transfers': incoming_transfers,
            'transfer_history': transfer_history
        }
    except Owner.DoesNotExist:
        user_owner = Owner.objects.create(user=request.user)
        context = {
            'animals': [],
            'pending_transfers': [],
            'incoming_transfers': [],
            'transfer_history': []
        }
    
    return render(request, 'profile/ownership.html', context)

@login_required
def process_transfer(request, transfer_id, action):
    """Process an ownership transfer (accept, reject, cancel)"""
    transfer = get_object_or_404(OwnershipTransfer, id=transfer_id)
    
    # Verify the user has permission to perform this action
    user_owner = get_object_or_404(Owner, user=request.user)
    
    if action == 'accept' and transfer.recipient == user_owner and transfer.status == 'pending':
        # Update animal ownership
        animal = transfer.animal
        animal.owner = transfer.recipient
        animal.save()
        
        # Update transfer status
        transfer.status = 'completed'
        transfer.completed_date = timezone.now()  # Using completed_date instead of updated_at
        transfer.save()
        
        # Create notification for sender
        Notification.objects.create(
            recipient=transfer.sender.user,
            message=f"Your transfer of {animal.tag_number} to {transfer.recipient.user.username} has been accepted.",
            link=f"/ownership/"
        )
        
        messages.success(request, f"You've accepted ownership of {animal.tag_number}.")
        
    elif action == 'reject' and transfer.recipient == user_owner and transfer.status == 'pending':
        # Update transfer status
        transfer.status = 'rejected'
        transfer.completed_date = timezone.now()  # Using completed_date instead of updated_at
        transfer.save()
        
        # Create notification for sender
        Notification.objects.create(
            recipient=transfer.sender.user,
            message=f"Your transfer of {transfer.animal.tag_number} to {transfer.recipient.user.username} has been rejected.",
            link=f"/ownership/"
        )
        
        messages.info(request, f"You've rejected ownership of {transfer.animal.tag_number}.")
        
    elif action == 'cancel' and transfer.sender == user_owner and transfer.status == 'pending':
        # Update transfer status
        transfer.status = 'cancelled'
        transfer.completed_date = timezone.now()  # Using completed_date instead of updated_at
        transfer.save()
        
        # Create notification for recipient if they exist
        if transfer.recipient:
            Notification.objects.create(
                recipient=transfer.recipient.user,
                message=f"Transfer of {transfer.animal.tag_number} from {transfer.sender.user.username} has been cancelled.",
                link=f"/ownership/"
            )
        
        messages.info(request, f"You've cancelled the transfer of {transfer.animal.tag_number}.")
        
    else:
        messages.error(request, "Invalid transfer action.")
    
    return redirect('ownership')

@login_required
def notifications(request):
    """View to display user notifications"""
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    context = {
        'notifications': user_notifications,
        'unread_count': user_notifications.filter(is_read=False).count()
    }
    return render(request, 'profile/notifications.html', context)

@login_required
def mark_notification_read(request):
    """API to mark a notification as read"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        notification_id = request.POST.get('notification_id')
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def mark_all_read(request):
    """Mark all notifications as read for the current user"""
    if request.method == 'POST':
        try:
            Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
            messages.success(request, "All notifications have been marked as read.")
        except Exception as e:
            messages.error(request, f"Failed to mark notifications as read: {str(e)}")
    
    return redirect('notifications')

@login_required
def health_records(request):
    """View for managing health records of animals"""
    try:
        user_owner = Owner.objects.get(user=request.user)
        animals = Animal.objects.filter(owner=user_owner)
        
        selected_animal_id = request.GET.get('animal_id')
        selected_animal = None
        health_records = []
        
        if selected_animal_id:
            selected_animal = get_object_or_404(Animal, id=selected_animal_id, owner=user_owner)
            health_records = HealthRecord.objects.filter(animal=selected_animal).order_by('-record_date')
        
            # Make sure health_records remains a QuerySet not a list
            vaccination_count = health_records.filter(record_type='vaccination').count()
            treatment_count = health_records.filter(record_type='treatment').count()
            checkup_count = health_records.filter(record_type='checkup').count()
            other_count = health_records.filter(record_type='other').count()
            
            if vaccination_count > 0:
                latest_vaccination = health_records.filter(record_type='vaccination').order_by('-record_date').first()
                if latest_vaccination and (datetime.now().date() - latest_vaccination.record_date).days <= 180:
                    vaccination_status = 'Up-to-date'
                    vaccination_percentage = 100
                else:
                    vaccination_status = 'Due for vaccination'
                    vaccination_percentage = max(0, 100 - ((datetime.now().date() - (latest_vaccination.record_date if latest_vaccination else datetime.now().date() - timedelta(days=180))).days / 180) * 100)
                    vaccination_percentage = min(100, max(0, vaccination_percentage))
            else:
                vaccination_status = 'Unknown'
                vaccination_percentage = 0
            
            last_checkup = health_records.filter(record_type='checkup').order_by('-record_date').first()
            last_checkup_date = last_checkup.record_date if last_checkup else None
            
            today = datetime.now().date().isoformat()
        else:
            # Set default values when no animal is selected
            vaccination_count = 0
            treatment_count = 0
            checkup_count = 0
            other_count = 0
            vaccination_status = 'Unknown'
            vaccination_percentage = 0
            last_checkup_date = None
            today = datetime.now().date().isoformat()
        
        context = {
            'animals': animals,
            'selected_animal': selected_animal,
            'health_records': health_records,
            'vaccination_count': vaccination_count,
            'treatment_count': treatment_count,
            'checkup_count': checkup_count,
            'other_count': other_count,
            'vaccination_status': vaccination_status,
            'vaccination_percentage': vaccination_percentage,
            'last_checkup_date': last_checkup_date,
            'today': today,
        }
    except Owner.DoesNotExist:
        context = {
            'animals': [],
            'health_records': [],
            'vaccination_count': 0,
            'treatment_count': 0,
            'checkup_count': 0,
            'other_count': 0,
            'vaccination_status': 'Unknown',
            'vaccination_percentage': 0,
            'last_checkup_date': None,
            'today': datetime.now().date().isoformat(),
        }
    
    return render(request, 'healths/health_record.html', context)

# Add health record view
def add_health_record(request, animal_id):
    return redirect('health_records')

# Edit health record view
def edit_health_record(request, record_id):
    return redirect('health_records')

# Delete health record view
def delete_health_record(request, record_id):
    return redirect('health_records')

# Get health record API
def get_health_record(request, record_id):
    return JsonResponse({'success': True})

# Helper function for admin/staff check
def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@user_passes_test(is_admin_or_staff)
def user_management(request):
    """View for user management"""
    search_query = request.GET.get('search', '')
    verified_filter = request.GET.get('verified', '')
    users = CustomUser.objects.all().order_by('-date_joined')
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if verified_filter == 'True':
        users = users.filter(is_verified=True)
    elif verified_filter == 'False':
        users = users.filter(is_verified=False)
    
    verified_count = users.filter(is_verified=True).count()
    context = {
        'users': users,
        'verified_count': verified_count,
        'search_query': search_query,
        'verified_filter': verified_filter
    }
    
    return render(request, 'users/users.html', context)

@csrf_exempt
@user_passes_test(is_admin_or_staff)
def toggle_user_verification(request, user_id):
    if request.method == 'POST':
        try:
            try:
                data = json.loads(request.body)
                verified = data.get('verified', False)
            except:
                verified = request.POST.get('verified', 'false').lower() == 'true'
            user = get_object_or_404(CustomUser, id=user_id)
            user.is_verified = verified
            user.save()
            return JsonResponse({'success': True, 'verified': user.is_verified})
        except:
            return JsonResponse({'success': False}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
@user_passes_test(is_admin_or_staff)
def get_user_details(request, user_id):
    """API to get detailed user information"""
    if request.method == 'GET':
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            try:
                animals_count = Animal.objects.filter(owner__user=user).count()
            except:
                animals_count = 0
                
            try:
                health_records_count = HealthRecord.objects.filter(animal__owner__user=user).count()
            except:
                health_records_count = 0
                
            try:
                transfer_count = OwnershipTransfer.objects.filter(
                    Q(sender__user=user) | Q(recipient__user=user)
                ).count()
            except:
                transfer_count = 0
            
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': f"{user.first_name} {user.last_name}".strip(),
                'profile_pic': user.profile_pic.url if hasattr(user, 'profile_pic') and user.profile_pic else None,
                'phone_number': getattr(user, 'phone_number', None),
                'address': getattr(user, 'address', None),
                'date_joined': user.date_joined.strftime('%b %d, %Y'),
                'last_login': user.last_login.strftime('%b %d, %Y') if user.last_login else None,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'is_verified': getattr(user, 'is_verified', False),
                'is_active': user.is_active,
                'animals_count': animals_count,
                'health_records_count': health_records_count,
                'transfer_count': transfer_count
            }
            return JsonResponse({
                'success': True,
                'user': user_data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

# Disable user API
@csrf_exempt
@user_passes_test(is_admin_or_staff)
def disable_user(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            
            if user.is_superuser:
                return JsonResponse({'success': False, 'error': 'Cannot disable admin accounts'}, status=403)
            
            user.is_active = False
            user.save()
            
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

# Toggle user status API
@csrf_exempt
@user_passes_test(is_admin_or_staff)
def toggle_user_status(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            try:
                data = json.loads(request.body)
                active = data.get('active', True)
            except:
                active = request.POST.get('active', 'true').lower() == 'true'
            
            if user.is_superuser and not active:
                return JsonResponse({'success': False, 'error': 'Cannot disable admin accounts'}, status=403)
            
            user.is_active = active
            user.save()
            return JsonResponse({'success': True, 'active': user.is_active})
        except:
            return JsonResponse({'success': False}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

# Form-based toggle user verification
@user_passes_test(is_admin_or_staff)
def toggle_user_verification_form(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        verified = request.POST.get('verified') == 'true'
        user.is_verified = verified
        user.save()
        
        action = "verified" if verified else "unverified"
        messages.success(request, f"User {user.username} has been {action}.")
    
    return redirect('user_management')

# Support request view
def support_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        request_type = request.POST.get('request_type')
        message = request.POST.get('message')
        
        SupportRequest.objects.create(
            username=username,
            email=email,
            request_type=request_type,
            message=message
        )
        
        messages.success(request, "Your support request has been submitted successfully.")
        return redirect('home')
    
    return render(request, 'support/support_request.html')

# Support requests list view
@user_passes_test(is_admin_or_staff)
def support_requests_list(request):
    requests = SupportRequest.objects.all().order_by('-created_at')
    pending_count = requests.filter(status='pending').count()
    
    context = {
        'requests': requests,
        'pending_count': pending_count,
    }
    
    return render(request, 'support/support_requests_list.html', context)

# Support request detail view
@user_passes_test(is_admin_or_staff)
def support_request_detail(request, request_id):
    request_obj = get_object_or_404(SupportRequest, id=request_id)
    
    try:
        user_obj = CustomUser.objects.get(username=request_obj.username)
    except:
        user_obj = None
    
    if request.method == 'POST':
        request_obj.status = request.POST.get('status')
        request_obj.admin_notes = request.POST.get('admin_notes')
        request_obj.save()
        
        messages.success(request, "Support request updated successfully.")
        return redirect('support_request_detail', request_id=request_id)
    
    context = {
        'request_obj': request_obj,
        'user_obj': user_obj
    }
    
    return render(request, 'support/support_request_detail.html', context)