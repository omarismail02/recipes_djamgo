from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,Userform, profileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.views import View
from main.models import Recipe,LikedRecipes
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            messages.success(request, f'You have successfully logged in!')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, f'You have been logged out!!')
    return redirect('hello')

@method_decorator(login_required, name='dispatch')
class profileview(View):

    def get(self, request):
        user_recipes = Recipe.objects.filter(cooker = request.user)
        user_liked_recipes = LikedRecipes.objects.filter(profile = request.user.profile)
        user_form = Userform(instance=request.user)
        profile_form = profileForm(instance=request.user.profile)
        return render (request, 'users/profile.html', {'user_form':user_form,
                                                       'profile_form':profile_form,
                                                       'user_recipes':user_recipes,
                                                       'user_liked_recipes': user_liked_recipes})
    
    def post(self, request):
        user_recipes = Recipe.objects.filter(cooker = request.user)
        user_liked_recipes = LikedRecipes.objects.filter(profile = request.user.profile)

        user_form = Userform(request.POST,instance=request.user)
        profile_form = profileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Profile updated successfully!')
            return redirect('home')
        else:
            messages.error(request,f'Error updating profile')
        return render (request, 'users/profile.html', {'user_form':user_form,
                                                       'profile_form':profile_form,
                                                       'user_recipes':user_recipes,
                                                       'user_liked_recipes': user_liked_recipes})
    



