from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Owner, Animal, OwnershipTransfer, HealthRecord, CustomUser, Species, Breed

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Verification', {'fields': ('is_verified', 'animal_expertise')}),
        ('Additional Info', {'fields': ('phone_number', 'address', 'profile_pic')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Owner)
admin.site.register(Animal)
admin.site.register(HealthRecord)

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'species')
    list_filter = ('species',)
    search_fields = ('name',)

@admin.register(OwnershipTransfer)
class OwnershipTransferAdmin(admin.ModelAdmin):
    list_display = ('animal', 'sender', 'recipient_email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('animal__tag_number', 'recipient_email')
    date_hierarchy = 'created_at'
