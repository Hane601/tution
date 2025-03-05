from django.contrib import admin
from .models import Member
from .models import register, student, Tutor
from django.contrib.auth.admin import UserAdmin
from django import forms
import random
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.html import format_html


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):

    fieldsets =(
        ('Personal details', {
            'fields': ('username', 'contact', 'password')
            }),
        ('Subjects', {
            'fields': ('English','Maths','Science','Sinhala','Buddhism','History',),
        }),
        ('Institute', {
        'fields':('Kakirihena','Mahaoya'),
        }),
        ('QR code',{
            'fields': ('qr',),
            }),
    )

    #readonly_fields = ('qr',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    readonly_fields = ('student_id', 'qr_preview', 'qr')  # QR preview and student_id are not editable
    search_fields = ['student_id', 'firstname']
    list_display = ('student_id', 'firstname', 'lastname', 'qr_preview')  # Show QR preview in list

    fieldsets = (
        (None, {
            'fields': ('student_id', 'firstname', 'lastname', 'phone'),
        }),
        ('Institute', {
            'fields': ('Mahaoya', 'Kakirihena'),
            'description': 'Select the Institute.',
        }),
        ('Subjects', {
            'fields': ('English', 'Maths', 'Science', 'Sinhala', 'Buddhism', 'History'),
        }),
        ('Year', {
            'fields': ('year',),
            'description': 'O/L year of student',
        }),
        ('QR Code', {
            'fields': ('qr_preview', 'qr'),  # Add QR preview and the actual QR image field
            'description': 'Generated QR code for the student',
        }),
    )

    def save_model(self, request, obj, form, change):
        """Overrides the save_model method to generate a unique student ID and QR code."""
        if not change:  # Only generate a student ID for new students
            self.generate_student_id(obj)
        
        # Generate and save the QR code
        self.generate_qr_code(obj)

        super().save_model(request, obj, form, change)

    def generate_student_id(self, obj):
        """Generates a unique student ID in the format 'spyXXXX'."""
        while True:
            four_digit_number = random.randint(1000, 9999)  # Ensure it's always 4 digits
            stu_id = f"spy{four_digit_number}"
            if not Member.objects.filter(student_id=stu_id).exists():
                obj.student_id = stu_id
                break

    def generate_qr_code(self, obj):
        """Generates a QR code based on the student ID and saves it as an image."""
        if obj.student_id:
            qr = qrcode.make(obj.student_id)
            qr_io = BytesIO()
            qr.save(qr_io, format='PNG')

            obj.qr.save(f'{obj.student_id}.png', ContentFile(qr_io.getvalue()), save=False)

    def qr_preview(self, obj):
        """Displays a preview of the QR code in the Django admin panel."""
        if obj.qr:
            return format_html('<img src="{}" width="150" height="150" />', obj.qr.url)
        return "No QR code"

    qr_preview.short_description = "QR Code Preview"  # Admin panel column name

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not obj:  # Only set student_id for new objects
            students = Member.objects.all()
            largest_number = -1

            # Find the largest existing 4-digit number in student_id
            for student in students:
                ids = student.student_id
                if ids and len(ids) > 3:  # Ensure student_id has at least 4 characters
                    try:
                        number = int(ids[-4:])  # Extract the last 4 digits
                        largest_number = max(largest_number, number)
                    except ValueError:
                        pass  # Ignore errors

            # Generate a new student_id
            if largest_number != -1:
                new_student_id = f"spy{largest_number + 1}"
            else:
                new_student_id = f"spy{random.randint(1000, 9999)}"  # First student case

            # Assign the new student_id to the form field
            if 'student_id' in form.base_fields:  # Check if student_id exists in form
                form.base_fields['student_id'].initial = new_student_id
            else:
                print("Warning: student_id not found in form.base_fields")  # Debugging

        return form

class studentInline(admin.TabularInline):
    model = student
    extra = 0  # Number of blank subfield rows to show by default
    readonly_fields = ('student_id', 'name', 'specific_class')  # Make these fields read-only
    can_delete = False  # Prevent deletion if required
    list_filter = ('specific_class',)
    def has_add_permission(self, request, obj=None):
        # Prevent adding new inline SubModel records
        return False
    class Media:
        js = ('admin/js/inline_search.js',)  # Load the custom JS file

@admin.register(register)
class registerAdmin(admin.ModelAdmin):
    inlines = [studentInline]
    search_fields = ['dates',]
    readonly_fields = ('dates',)
    list_display = ('dates',)
    can_delete = False
    def has_add_permission(self, request, obj=None):
    # Prevent adding new inline SubModel records
        return False

