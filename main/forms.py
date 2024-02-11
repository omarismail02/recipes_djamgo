from django import forms

from .models import Recipe

class recipe_form(forms.ModelForm):
    class Meta:
          model = Recipe
          fields = {'title','ingredients','instructions','cooking_time',
                    'servings','nutritional_information','image'}
