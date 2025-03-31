from django.shortcuts import  render, redirect
from django.contrib import messages

from grievance_portal.models import Query, Student, Complaint

def signup(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        prn = request.POST["prn"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        department = request.POST["department"]
        course = request.POST["course"]
        admission_year = request.POST["admission_year"]
        graduation_year = request.POST["graduation_year"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if Student.objects.filter(prn=prn).exists():
            messages.error(request, "PRN already registered!")
            return redirect("signup")

        student = Student.objects.create(
            full_name=full_name, prn=prn, email=email, mobile=mobile,
            department=department, course=course, admission_year=admission_year,
            graduation_year=graduation_year, dob=dob, gender=gender,
            address=address, password=password
        )
        student.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "signup.html")



#login
def login(request):
    if request.method == 'POST':
        prn = request.POST['username']
        password = request.POST['password']

        try:
            student = Student.objects.get(prn=prn)     # Fetch student by PRN
            if password == student.password:           # Verify password 
                request.session['prn'] = prn
                request.session['password'] = password
                request.session['is_logged_in'] = True
                return render(request,'home.html', {"student":student})                # Redirect to home page
            else:
                messages.error(request, "Invalid Password")
        except Student.DoesNotExist:
            messages.error(request, "Invalid Username")

    return render(request, 'login.html')



#forgot 
def forgot_password(request):
    if request.method == 'POST':
        prn = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
        else:
            try:
                student = Student.objects.get(prn=prn)  # Check if PRN exists
                student.password = new_password  # Save  password
                student.save()

                messages.success(request, "Password successfully reset! You can now log in.")
                return redirect('login')  # Redirect to login page

            except Student.DoesNotExist:
                messages.error(request, "Username not found! Please enter a valid Username.")

    return render(request, 'forgot_password.html')




#home
def home(request):
    prn=request.session.get("prn")
    student = Student.objects.get(prn=prn)
    return render(request,'home.html', {"student":student}) 


#file a complaint
def file_complaint(request):
    if request.method == "POST":
        prn = request.session.get("prn")  #  Get PRN from session
        if not prn:
            messages.error(request, "Session expired! Please log in again.")
            return redirect("login")  

        # Get form data
        complaint_type = request.POST["complaint_type"]
        title = request.POST["title"]
        description = request.POST["description"]
        anonymous = "anonymous" in request.POST  # Check if checkbox is checked

        #  Save complaint with PRN 
        if anonymous:
            Complaint.objects.create(
            complaint_type=complaint_type,
            title=title,
            description=description,
            anonymous=anonymous
        )
        else:
            Complaint.objects.create(
            prn_id=prn,                           #  Pass PRN directly (ForeignKey will link it)
            complaint_type=complaint_type,
            title=title,
            description=description,
            anonymous=anonymous
        )

        return redirect("view_complaints")  

    return render(request, "file_complaint.html")



#view complaints
def view_complaints(request):
    prn = request.session.get("prn")  # Get PRN from session
    if not prn:
        return redirect("login")  # Redirect if session expired

    complaints = Complaint.objects.filter(prn_id=prn).order_by("-created_at")  # Fetch complaints

    return render(request, "view_complaints.html", {"complaints": complaints})



#manage a complaints
def manage_complaints(request):
    prn = request.session.get("prn")
    if not prn:
        messages.error(request, "Session expired! Please log in again.")
        return redirect("login") 

    complaints = Complaint.objects.filter(prn_id=prn).order_by("-created_at")
    return render(request, "manage_complaints.html", {"complaints": complaints})

#withdraw  complaint
def withdraw_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)

    if complaint.status == "Pending":
        complaint.delete()

    return redirect("manage_complaints")


#edit complaint
def edit_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    complaint_types = ["Academic", "Hostel", "Mess", "Facilities", "Faculties", "Canteen", "Others"]

    
    if request.method == "POST":
        prn = request.session.get("prn")  #  Get PRN from session
        if not prn:
            messages.error(request, "Session expired! Please log in again.")
            return redirect("login")  

        # Get form data
        complaint_type = request.POST["complaint_type"]
        title = request.POST["title"]
        description = request.POST["description"]
        anonymous = "anonymous" in request.POST  # Check if checkbox is checked

        #  Save complaint with PRN 
        if anonymous:
            complaint.complaint_type=complaint_type
            complaint.title=title
            complaint.description=description
            complaint.anonymous=anonymous
            complaint.save()
        else:
            complaint.complaint_type=complaint_type
            complaint.title=title
            complaint.description=description
            complaint.prn_id=prn
            complaint.save()

        complaints = Complaint.objects.filter(prn_id=prn).order_by("-created_at")
        return render(request,"view_complaints.html", {"complaints": complaints}) 

    if complaint.status == "Pending":
        return render(request, 'edit_complaint.html', {'complaint':complaint, 'complaint_types':complaint_types}) 
    
    return render(request, 'edit_complaint.html')
    

#base
def base(request):
    return render(request, 'base.html')

#about
def about(request):
    return render(request, 'aboutus.html')

#query
def query(request):
    if request.method == "POST":
        prn = request.session.get("prn")

        if not prn:
            messages.error(request, "Session expired! Please log in again.")
            return redirect("login")
        
        title = request.POST["title"]
        description = request.POST["description"]
        query_type = request.POST["query_type"]
        module = request.POST["module"]
        url = request.POST.get("url", "")
        evidence = request.FILES.get("evidence", None)

        Query.objects.create(
            prn_id=prn,
            title=title,
            description=description,
            query_type=query_type,
            module=module,
            url=url,
            evidence=evidence,
            status="Pending",
        )

        queries = Query.objects.filter(prn_id=request.session.get("prn")).order_by("-created_at")
        return render(request, "query.html", {"queries": queries})

    queries = Query.objects.filter(prn_id=request.session.get("prn")).order_by("-created_at")
    return render(request, "query.html", {"queries": queries})


def student_logout(request):
    request.session.flush()  # Clears all session data
    request.session["prn"]=""
    request.session["password"]=""
    del request.session["prn"]
    del request.session["password"]
    response = redirect('login')  # Redirect to login page
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

#profile
def profile(request):
    prn = request.session.get("prn")  # Get PRN from session
    if not prn:
        messages.error(request, "Session expired! Please log in again.")
        return redirect("login")

    student = Student.objects.get(prn=prn)  # Fetch Student Data

    if request.method == "POST":
        email = request.POST.get("email", "")
        mobile = request.POST.get("mobile", "")
        address = request.POST.get("address", "")

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if old_password and new_password and confirm_password:
            if old_password != student.password:
                messages.error(request, "Incorrect old password!")
                return redirect("profile")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match!")
                return redirect("profile")
            else:
                student.password = new_password
                student.save()
                messages.success(request, "Password changed successfully!")
                return redirect("profile")

        if email:
            student.email = email
        if mobile:
            student.mobile = mobile
        if address:
            student.address = address

        student.save()
        messages.success(request, "Profile updated successfully!")
        

        return redirect("profile")

    return render(request, "profile.html", {"student": student})