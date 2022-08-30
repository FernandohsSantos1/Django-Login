from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect

def home(request):
    if request.session.get('logado') == True:
        return render(request, 'home.html')
    else:
        messages.add_message(request, constants.WARNING, 'Realize o login para ter acesso ao sistema!')
        return redirect('/auth/login/')