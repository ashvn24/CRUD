from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def loginpage(request):
    if 'username' in request.session:
        return redirect('home')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            if not username and not password:  # Check if both username and password are blank
                messages.error(request, "Please enter a username and password.")
                return redirect('login')
        
            user=auth.authenticate(username=username,password=password)
            
            if user is not None:
                request.session['username'] = username
                login(request,user)
                return redirect('home')
            else:
                user_exists = User.objects.filter(username=username).exists()
                if user_exists:
                    messages.error(request, "Incorrect password")
                else:
                    messages.error(request, "Invalid username and password")
                return redirect('login')
        else:
            return render(request,'login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache       
def signup(request):
    if 'username' in request.session:
        return redirect('home')
    elif request.method=='POST':
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm=request.POST.get('confirmpassword')
        if not (username and email and password and confirm and first_name and last_name):
                messages.info(request,"Please fill required feild")
                return redirect('signup')
        elif password != confirm:
                messages.info(request,"Password mismatch")
                return redirect('signup')
        else:
            if User.objects.filter(username = username).exists():
                messages.info(request,"Username Already Taken")
                return redirect('signup')
            elif User.objects.filter(email = email).exists():
                 messages.info(request,"Email Already Taken")
                 return redirect('signup')
            else:
                user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                user.set_password(password)
                user.save()
                
        return redirect('login')
           
    return render(request,'signup.html')

@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def home(request):
    return render(request,'home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def logout(request):
    if 'username' in request.session:
        del request.session['username']
        auth.logout(request)
        return redirect('login')
    

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def crudadmin(request):
    if 'username' in request.session:
        return redirect('home')
    elif 'crud' in request.session:
        return redirect('dashboard')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password=request.POST.get('password')
            user=auth.authenticate(username=username,password=password)
            if user is not None and user.is_superuser:
                request.session['crud']=username
                login(request,user)
                return redirect('dashboard')
            else:
                messages.info(request,"Invalid Credentials")
            
    return render(request,'crudadmin.html')       

@login_required(login_url='crud')
@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def dashboard(request):
    if 'crud' in request.session:
        users = User.objects.filter(is_staff= False)
        context = {
            'users': users,
        }
        return render(request, 'dashboard.html', context)
    return redirect('users')
    
    
def add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')


        user = User.objects.create_user(
            username = name,
            email    = email,
            password = password,
            first_name=first_name,
            last_name=last_name,
            
        )
        
        return redirect('dashboard')
    
    return render(request,'dashboard.html')

def edit(request):
    user = user.objects.all()

    context = {
        'user' : user,

    }


    return redirect(request,'dashboard.html',context)

def update(request, id):
    
    user = User.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        user.username = name
        user.email = email
        user.first_name=first_name
        user.last_name=last_name
        if password:
            user.set_password(password)
        user.save()
        return redirect('dashboard')
    else:
        context = {
            'user': user
        }
        return render(request, 'dashboard.html', context)
    

def delete(request,id):
    des = User.objects.filter(id=id)
    des.delete()
    return redirect( 'dashboard')

def search(request):
    query = request.GET.get('q')
    if query :
        results = User.objects.filter(username__icontains=query).exclude(username='admin')   
    else:
        results = []
    context = {
        'users': results,
        'query': query,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='crud')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def admin_logout(request):
    if 'crud' in request.session:
        del request.session['crud']
        auth.logout(request)
    return redirect('crud')