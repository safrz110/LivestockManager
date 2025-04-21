from .models import Notification, SupportRequest

def notification_processor(request):
    context = {}
    
    if request.user.is_authenticated:
        # Get unread notifications count
        try:
            unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
            context['unread_notifications'] = unread_count
        except Exception:
            # If for some reason notifications can't be fetched, don't break the site
            context['unread_notifications'] = 0
        
        # Add pending support requests count for staff/admin
        if request.user.is_staff or request.user.is_superuser:
            try:
                pending_count = SupportRequest.objects.filter(status='pending').count()
                context['pending_support_requests'] = pending_count
            except Exception:
                context['pending_support_requests'] = 0
    
    return context
