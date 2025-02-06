from django.shortcuts import render
from .models import Recipe
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import RecipeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    recipes = Recipe.objects.order_by('?')[:5]
    return render(request, 'recipes/home.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            # Если пользователь не аутентифицирован, используем "анонимного" пользователя
            if request.user.is_authenticated:
                recipe.author = request.user
            else:
                anonymous_user, created = User.objects.get_or_create(username='Anonymous')
                recipe.author = anonymous_user
            recipe.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

def custom_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('home')
from django.shortcuts import render
