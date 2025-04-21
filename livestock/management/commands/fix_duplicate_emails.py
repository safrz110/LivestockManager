from django.core.management.base import BaseCommand
from django.db.models import Count
from livestock.models import CustomUser

class Command(BaseCommand):
    help = 'Fix duplicate email addresses'

    def handle(self, *args, **options):
        # Find users with duplicate emails
        duplicates = (
            CustomUser.objects.values('email')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
            .values_list('email', flat=True)
        )

        if not duplicates:
            self.stdout.write(self.style.SUCCESS('No duplicate emails found!'))
            return

        self.stdout.write(self.style.WARNING(f'Found {len(duplicates)} duplicate email(s)'))

        for email in duplicates:
            users = CustomUser.objects.filter(email=email).order_by('date_joined')
            self.stdout.write(f'\nDuplicate email: {email}')
            
            # Keep the first user's email unchanged
            original_user = users[0]
            self.stdout.write(f'Keeping original user: {original_user.username}')
            
            # Update other users' emails
            for i, user in enumerate(users[1:], 1):
                new_email = f'{email.split("@")[0]}+{i}@{email.split("@")[1]}'
                user.email = new_email
                user.save()
                self.stdout.write(f'Updated {user.username} email to: {new_email}')
