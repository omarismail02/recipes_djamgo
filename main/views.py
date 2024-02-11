from django.shortcuts import render,redirect, get_object_or_404
from .models import Recipe, LikedRecipes
from .forms import recipe_form
from django.contrib import messages
from .filters import RecipeFilter
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def hello_world(request):
    return render(request, 'main/template.html')

def about(request):
    return render(request, 'main/about.html')

@login_required
def home_view(request):
    recipes = Recipe.objects.all()
    recipe_filter = RecipeFilter(request.GET, queryset= recipes)
    user_liked_recipes = LikedRecipes.objects.filter(
        profile = request.user.profile).values_list('recipe')
    liked_recipes_ids = [ r[0] for r in user_liked_recipes ]
    print(liked_recipes_ids)
    context = {
        'recipe_filter':recipe_filter,
        'liked_recipes_ids':liked_recipes_ids
    }
    return render(request, 'main/home.html', context)

@login_required
def recipe_view(request):
    if request.method == "POST":
        try:
            recipe = recipe_form(request.POST, request.FILES)
            if recipe.is_valid():
                recipe.instance.cooker = request.user
                recipe.save()
                messages.info(request,f'{recipe.cleaned_data["title"]} posted successfully!!')
                return redirect ('home')
            else:
                raise Exception
        except Exception as e:
            print(e)
            messages.error(request,f'An error has occured while creating the recipe')

    elif request.method == "GET":
        recipe = recipe_form()
    return render(request, 'main/recipe.html',{'recipe': recipe})

@login_required
def view_view(request,id):
    try:
        recipe = Recipe.objects.get(id = id)
        if recipe is None:
            raise Exception
        return render(request, 'main/view.html',{'recipe': recipe})
    except Exception as e:
        messages.error(request,f'Invald id {id} was provided for recipe!')
        return redirect('home')


@login_required   
def edit_view(request, id):
    try:
      recipe = Recipe.objects.get(id=id)
      if recipe is None:
            raise Exception
      if request.method == 'POST':
            recipe_fo = recipe_form(
                request.POST, request.FILES, instance= recipe)
            if recipe_fo.is_valid():
                recipe_fo.save()
                messages.info(request, f'recipe {id} updated successfully!!')
                return redirect('home')
            else:
              messages.error(request, f'An error occured while trying to edit the recipe') 
      else:
          recipe_fo = recipe_form(instance= recipe)
      return render(request, 'main/edit.html', {'recipe_fo': recipe_fo})
    except Exception as e :
        messages.error(request, f'An error occured while trying to access this recipe page')
    return redirect('home')

@login_required   
def Like_recipe_view(request, id):
    recipe_like = get_object_or_404(Recipe, id = id)

    liked_recipe, created = LikedRecipes.objects.get_or_create(profile = request.user.profile,
                                                       recipe = recipe_like)
    if not created:
        liked_recipe.delete()
    else:
        liked_recipe.save()
    
    return JsonResponse({
        'is_liked_by_user':created,
    })
        

