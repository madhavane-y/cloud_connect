from django.shortcuts import render#,render_to_response
from .forms import log_form
from django.http import HttpResponseRedirect
from .models import account
from django.contrib import messages
# from django.core import 
# from .back_auth import auth
# from django.template import RequestContext 

# Create your views here.
def login_view(request):
    if(request.method == "POST"):
        login_form = log_form(request.POST)     # populate form with data
        if(login_form.is_valid()):
            # auths =auth()
            inst = login_form.cleaned_data
            # print(inst)    *******   DEBUG
            # au = auths.authenticate(inst['iam'],inst['alias'],inst['passwd'])
            if((inst['passwd'] == account.objects.get(alias=inst['alias']).passwd)): #and (inst['iam'] in account.objects.get(iam=inst('iam')))):
                request.session['cred']=[inst]
                return HttpResponseRedirect('/account')
            else:
                messages.add_message(request,messages.ERROR,'Incorrect credentials or password')
                return render(request,'login.html',{'form':login_form,'inc_cr':'Incorrect credentials or password'})
                # return HttpResponseRedirect(reverse('login:login'))
        else:
                return render(request,'login.html',{'form':login_form,'inc_cr':'Incorrect credentials or password'})

    else:
        login_form = log_form()
        # return render(request,'login.html')

    return render(request,'login.html',{'form':login_form,'inc_cr':''})