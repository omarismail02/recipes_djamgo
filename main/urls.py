from django.urls import path
from main.views import hello_world, home_view,recipe_view,view_view,edit_view,about,Like_recipe_view


urlpatterns = [
    path('', hello_world , name = 'hello'),
    path('home/', home_view , name = 'home'),
    path('about/', about , name = 'about'),
    path('recipe/', recipe_view , name = 'recipe'),
    path('view/<int:id>/', view_view , name = 'view'),
    path('edit/<int:id>/', edit_view , name = 'edit'),
    path('liked/<int:id>/', Like_recipe_view , name = 'Like'),

]