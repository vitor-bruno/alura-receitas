from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita
from django.core.paginator import Paginator

def cadastro(request):
    '''Cadastra um novo usuário no sistema'''
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha_2 = request.POST['password2']
        
        if campo_vazio(nome):
            messages.error(request, 'O campo nome não pode ficar em branco')
            return redirect('cadastro')
        
        if campo_vazio(email):
            messages.error(request, 'O campo e-mail não pode ficar em branco')
            return redirect('cadastro')
        
        if senhas_diferentes(senha, senha_2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso!')

        print(nome, email, senha, senha_2)
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    '''Realiza o login de um usuário no sistema'''
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso')
                return redirect('dashboard')
        
        else:
            messages.error(request, 'Usuário não cadastrado no sistema')
            return redirect('login')

    return render(request, 'usuarios/login.html')

def logout(request):
    '''Desconecta o usuário do sistema'''
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    '''Renderiza a área do usuário logado'''
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=request.user.id)

        paginator = Paginator(receitas, 3)
        page = request.GET.get('page')
        receitas_por_pagina = paginator.get_page(page)

        return render(request, 'usuarios/dashboard.html', {'receitas' : receitas_por_pagina})
    else:
        return redirect('index')

def campo_vazio(campo):
    '''Verifica se um campo não foi preenchido'''
    return not campo.strip()

def senhas_diferentes(senha, senha2):
    '''Verifica se duas senhas informadas são diferentes'''
    return senha != senha2