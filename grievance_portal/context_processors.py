from .models import Student

def student_info(request):
    if 'prn' in request.session:  # Check if session exists
        try:
            student = Student.objects.get(prn=request.session['prn'])  # Fetch student from DB
            return {
                'student': student  # Store the whole student object
            }
        except Student.DoesNotExist:
            return {}  # Return empty if student not found
    return {}  # Return empty if session does not exist
