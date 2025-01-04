from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserProfile,LoginTable


# Create your views here.

def  userRegistration(request):
     login_table=LoginTable()
     user_profile=UserProfile()
     if request.method=='POST':
          user_profile.username=request.POST['username']
          user_profile.password=request.POST['password']
          user_profile.cpassword=request.POST['cpassword']

          login_table.username=request.POST['username']
          login_table.password=request.POST['password']
          login_table.cpassword=request.POST['cpassword']
          login_table.type='user'

          if request.POST['password']==request.POST['cpassword']:
               user_profile.save()
               login_table.save()
               

               messages.info(request,'registration success')
               return redirect('login')
          
          else:
               messages.info(request,'password not matching')
               return redirect('register')
          

     return render(request,'register.html')




def loginpage(request):
      if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            user=LoginTable.objects.filter(username=username,password=password,type='user').exists()
            try:
                 if user is not None:
                      user_details=LoginTable.objects.get(username=username,password=password)
                      user_name=user_details.username
                      type=user_details.type
                      

                      if type=='user':
                           request.session['username']=user_name
                           return redirect('userview')
                      
                      elif type=='admin':
                           request.session['username']=user_name
                           return redirect('destination_list')
                      
                 else:       
                    messages.error(request,'invalid username or password')
            except:
                   messages.error(request,'invalid role')
      return render(request,'login.html')



def logout_view(request):
     logout(request)
     return redirect('login')
