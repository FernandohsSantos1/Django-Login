from django.shortcuts import render
from django.db.models import Q
from .models import Usuario
from django.shortcuts import redirect
from hashlib import sha256
from django.contrib import messages
from django.contrib.messages import constants

def login(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    con_senha = request.POST.get('con_senha')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        messages.add_message(request, constants.WARNING, 'Cadastro inválido! Nome ou email em branco!')
        return redirect('/auth/cadastro/')

    if len(senha) < 8:
        messages.add_message(request, constants.WARNING, 'Cadastro inválido! Senha menor que 8 digitos!')
        return redirect('/auth/cadastro/')
    
    if senha != con_senha:
        messages.add_message(request, constants.WARNING, 'Cadastro inválido! As senhas informadas não correspondem!')
        return redirect('/auth/cadastro/')

    usuario = Usuario.objects.filter(email = email)
    
    if len(usuario) > 0:
        messages.add_message(request, constants.WARNING, 'Cadastro inválido! Email já está em uso!')
        return redirect('/auth/cadastro/')
    
    try:    
        senha = sha256(senha.encode()).hexdigest()
        novo_usuario = Usuario(nome = nome,
                            email = email,            
                            senha = senha)
        novo_usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso!')
        return redirect('/auth/cadastro/')
    except:
        messages.add_message(request, constants.ERROR, 'Cadastro inválido! Não foi possivel cadastrar no banco de dados!')
        return redirect('/auth/cadastro/')

def valida_login(request):
    nome_email = request.POST.get('nome')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(Q(nome = nome_email)|Q(nome = nome_email))
    if len(usuario) == 0:
        messages.add_message(request, constants.WARNING, 'Login inválido! Nome ou email incorreto!')
        return redirect('/auth/login/')
    
    usuario = Usuario.objects.filter(Q(nome = nome_email)|Q(nome = nome_email)).filter(senha = senha)
    if len(usuario) == 0:
        messages.add_message(request, constants.WARNING, 'Login inválido! Senha incorreta!')
        return redirect('/auth/login/')
    
    else:
        request.session['logado'] = True
        request.session['usuario_id'] = usuario[0].id
        return redirect('/plataforma/home/')

def sair(request):
    request.session.flush()
    messages.add_message(request, constants.INFO, 'Sessão encerrada com sucesso!')
    return redirect('/auth/login/')