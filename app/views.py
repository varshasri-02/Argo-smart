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
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

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
    result=''

    if request.method == 'POST':
        form = FindCropForm(request.POST)
            
        nitrogen = request.POST['nitrogen']
        phosphorus = request.POST['phosphorus']
        potassium = request.POST['potassium']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
        ph = request.POST['ph']
        rainfall = request.POST['rainfall']

        df = pd.read_csv("Machine Learning\Crop_recommendation.csv")

        features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
        target = df['label']

        acc = []
        model = []

        Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

        RF = RandomForestClassifier(n_estimators=20, random_state=0)
        RF.fit(Xtrain.values,Ytrain.values)

        predicted_values = RF.predict(Xtest.values)

        x = metrics.accuracy_score(Ytest, predicted_values)
        acc.append(x)
        model.append('RF')

        data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        prediction = RF.predict(data)
        result = "The predicted crop is "+ str(prediction).replace("'","")[1:-1]

    else:
        form=FindCropForm()
    return render(request, 'visitor/visitor_find_crop.html',{'form':form,'result':result})




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
