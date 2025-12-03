from unicodedata import category
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from pyparsing import empty
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

#<-----For check user is Admin and Visitor----->#
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_visitor(user):
    return user.groups.filter(name='VISITOR').exists()

#<-----LogOut For All----->#
@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect('/')

#<-------------------------------------------->#
#<---------------Admin Functions-------------->#
#<-------------------------------------------->#

#<-----Login For Admin----->#
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='ADMIN'):
                    login(request,user)
                    return redirect('admin_home')
                else:
                    messages.success(request, 'Your account is not found in Admin..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')
    else:
         form = AdminLoginForm()           
    return render(request, 'admin/admin_login.html',{'form':form})


#<-----Home Page for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_home(request):
    return render(request, 'admin/admin_home.html')

#<-----Profile Page for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_profile(request):
    return render(request, 'admin/admin_profile.html')

#<-----Change password----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def change_password_admin(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'admin/change_password_admin.html', {'form': form})

#<-----Admin Approvall for visitors----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_approve_visitor(request):
    visitors = Visitor.objects.all().filter(status=False)
    return render(request, 'admin/admin_approve_visitor.html',{'visitors':visitors})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def approve_visitor(request):
    visitor=get_object_or_404(Visitor, pk=request.GET.get('visitor_id'))
    visitor.status=True
    visitor.save()
    return redirect(reverse('admin_approve_visitor'))

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_visitor(request):
    visitor=get_object_or_404(Visitor, pk=request.GET.get('visitor_id'))
    user=User.objects.get(id=visitor.user_id)
    user.delete()
    visitor.delete()
    return redirect(reverse('admin_approve_visitor'))



#<-----Admin add Admin----->#
def admin_add_admin(request):
    if request.method=='POST':
        form1=AdminUserForm(request.POST)
        form2=AdminExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_admin_group=Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('admin_active_admin')
    else:
        form1=AdminUserForm()
        form2=AdminExtraForm()
    return render(request, 'admin/admin_add_admin.html',{'form1':form1,'form2':form2})

#<-----Active Admin View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_admin(request):
    admins = Admin.objects.all()
    return render(request, 'admin/admin_active_admin.html',{'admins':admins})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_admin_active(request):
    admin=get_object_or_404(Admin, pk=request.GET.get('admin_id'))
    user=User.objects.get(id=admin.user_id)
    user.delete()
    admin.delete()
    return redirect(reverse('admin_active_admin'))

#<-----Active Visitor View for Admin----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_active_visitor(request):
    visitors = Visitor.objects.all().filter(status=True)
    return render(request, 'admin/admin_active_visitor.html',{'visitors':visitors})

@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def delete_visitor_active(request):
    visitor=get_object_or_404(Visitor, pk=request.GET.get('visitor_id'))
    user=User.objects.get(id=visitor.user_id)
    user.delete()
    visitor.delete()
    return redirect(reverse('admin_active_visitor'))




#<---------------------------------------------->#
#<---------------Visitor Functions-------------->#
#<---------------------------------------------->#

#<-----Signup For Visitor----->#
def visitor_signup(request):
    if request.method=='POST':
        form1=VisitorUserForm(request.POST)
        form2=VisitorExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True  # Auto-approve new visitors
            user2=f2.save()

            my_visitor_group=Group.objects.get_or_create(name='VISITOR')
            my_visitor_group[0].user_set.add(user)

            messages.success(request, 'Account created successfully! You can now login.')

            return HttpResponseRedirect('/')
    else:
        form1=VisitorUserForm()
        form2=VisitorExtraForm()
    return render(request, 'visitor/visitor_signup.html',{'form1':form1,'form2':form2})

#<-----Login For Visitor----->#
def visitor_login(request):
    if request.method == 'POST':
        form = VisitorLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.groups.filter(name='VISITOR'):
                    if Visitor.objects.all().filter(user_id=user.id,status=True):
                        login(request,user)
                        return redirect('visitor_home')
                    else:
                       messages.success(request, 'Your Request is in process, please wait for Approval..') 
                else:
                    messages.success(request, 'Your account is not found in Visitor..')
            else:
                messages.success(request, 'Your Username and Password is Wrong..')
    else:
         form = VisitorLoginForm()           
    return render(request, 'visitor/visitor_login.html',{'form':form})

#<-----Home Page for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_home(request):
    return render(request, 'visitor/visitor_home.html')

#<-----Profile Page for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_profile(request):
    return render(request, 'visitor/visitor_profile.html')

#<-----Change password----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def change_password_visitor(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('visitor_home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'visitor/change_password_visitor.html', {'form': form})


#<-----Find Crop for Visitor----->#
@login_required(login_url='visitor_login')
@user_passes_test(is_visitor)
def visitor_find_crop(request):
    result = ''
    error_message = ''

    if request.method == 'POST':
        form = FindCropForm(request.POST)

        if form.is_valid():
            try:
                # Extract validated data
                nitrogen = form.cleaned_data['nitrogen']
                phosphorus = form.cleaned_data['phosphorus']
                potassium = form.cleaned_data['potassium']
                temperature = form.cleaned_data['temperature']
                humidity = form.cleaned_data['humidity']
                ph = form.cleaned_data['ph']
                rainfall = form.cleaned_data['rainfall']

                # Input validation ranges (based on dataset analysis)
                if not (0 <= nitrogen <= 140):
                    error_message = "Nitrogen level must be between 0 and 140"
                elif not (0 <= phosphorus <= 145):
                    error_message = "Phosphorus level must be between 0 and 145"
                elif not (0 <= potassium <= 205):
                    error_message = "Potassium level must be between 0 and 205"
                elif not (8.8 <= temperature <= 43.7):
                    error_message = "Temperature must be between 8.8°C and 43.7°C"
                elif not (14.3 <= humidity <= 99.98):
                    error_message = "Humidity must be between 14.3% and 99.98%"
                elif not (3.5 <= ph <= 9.9):
                    error_message = "pH value must be between 3.5 and 9.9"
                elif not (20.2 <= rainfall <= 298.6):
                    error_message = "Rainfall must be between 20.2 cm and 298.6 cm"
                else:
                    # Load pre-trained model and scaler
                    try:
                        model = joblib.load('crop_model.joblib')
                        scaler = joblib.load('scaler.joblib')
                    except FileNotFoundError:
                        error_message = "Model files not found. Please contact administrator."
                        return render(request, 'visitor/visitor_find_crop.html', {'form': form, 'error_message': error_message})

                    # Prepare input data
                    input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

                    # Scale the input
                    input_scaled = scaler.transform(input_data)

                    # Make prediction
                    prediction = model.predict(input_scaled)
                    predicted_crop = prediction[0]

                    result = f"The predicted crop is {predicted_crop}"

            except Exception as e:
                error_message = f"An error occurred during prediction: {str(e)}"
        else:
            error_message = "Please correct the errors in the form."
    else:
        form = FindCropForm()

    return render(request, 'visitor/visitor_find_crop.html', {
        'form': form,
        'result': result,
        'error_message': error_message
    })



#<-----API Endpoint for Crop Prediction----->#
@csrf_exempt
@require_http_methods(["POST"])
def predict_crop_api(request):
    """
    API endpoint for crop prediction.
    Accepts JSON with: nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall
    Returns JSON with prediction or error.
    """
    try:
        # Parse JSON data
        data = json.loads(request.body)

        # Extract parameters
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
        input_data = []

        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'error': f'Missing required field: {field}'
                }, status=400)
            try:
                value = float(data[field])
                input_data.append(value)
            except (ValueError, TypeError):
                return JsonResponse({
                    'error': f'Invalid value for {field}: must be a number'
                }, status=400)

        nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall = input_data

        # Input validation ranges
        validations = {
            'nitrogen': (0, 140),
            'phosphorus': (0, 145),
            'potassium': (0, 205),
            'temperature': (8.8, 43.7),
            'humidity': (14.3, 99.98),
            'ph': (3.5, 9.9),
            'rainfall': (20.2, 298.6)
        }

        for field, (min_val, max_val) in validations.items():
            value = locals()[field]
            if not (min_val <= value <= max_val):
                return JsonResponse({
                    'error': f'{field.capitalize()} must be between {min_val} and {max_val}'
                }, status=400)

        # Load model and scaler
        try:
            model = joblib.load('crop_model.joblib')
            scaler = joblib.load('scaler.joblib')
        except FileNotFoundError:
            return JsonResponse({
                'error': 'Model files not found. Please contact administrator.'
            }, status=500)

        # Prepare and scale input
        input_array = np.array([input_data])
        input_scaled = scaler.transform(input_array)

        # Make prediction
        prediction = model.predict(input_scaled)
        predicted_crop = prediction[0]

        # Get prediction probabilities if available
        try:
            probabilities = model.predict_proba(input_scaled)[0]
            crop_classes = model.classes_
            prob_dict = dict(zip(crop_classes, probabilities))
        except:
            prob_dict = None

        response = {
            'prediction': predicted_crop,
            'input_data': {
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }
        }

        if prob_dict:
            response['probabilities'] = prob_dict

        return JsonResponse(response)

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Internal server error: {str(e)}'
        }, status=500)


#<-----Signup For Admin (Protected - Only accessible by existing admins)----->#
@login_required(login_url='admin_login')
@user_passes_test(is_admin)
def admin_signup(request):
    if request.method=='POST':
        form1=AdminUserForm(request.POST)
        form2=AdminExtraForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_admin_group=Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            messages.success(request, 'New admin created successfully!')
            return redirect('admin_active_admin')
    else:
        form1=AdminUserForm()
        form2=AdminExtraForm()
    return render(request, 'admin/admin_signup.html',{'form1':form1,'form2':form2})
