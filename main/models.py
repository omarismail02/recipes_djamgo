from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    cooker = models.ForeignKey(User,on_delete = models.CASCADE)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField() # in minutes
    servings = models.PositiveIntegerField(default = 4)  
    nutritional_information = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add =True)
    date_updated = models.DateTimeField(auto_now =True)
    image = models.ImageField(upload_to='imges/')

    def __str__(self):
        return self.title
    

class LikedRecipes(models.Model):
    profile = models.ForeignKey(Profile, on_delete= models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete= models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.recipe.title} recipe liked by {self.profile.user.username}'
