import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','wad_recipe_book.settings')

import django
django.setup()

from recipes.models import Category, Recipe


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    italian = [
    # Italian Recipes
    {
        "title": "Margherita Pizza",
        "difficulty": "Medium",
        "description": "A classic Neapolitan pizza with tomato, mozzarella, and basil.",
        "ingredients": ["Pizza dough", "Tomato sauce", "Mozzarella", "Basil", "Olive oil", "Salt"],
        "instructions": "Roll out dough. Spread tomato sauce. Add mozzarella and basil. Bake at high temp."
    },
    {
        "title": "Lasagna",
        "difficulty": "Hard",
        "description": "A rich layered pasta dish with meat, béchamel sauce, and cheese.",
        "ingredients": ["Lasagna noodles", "Ground beef", "Tomato sauce", "Ricotta", "Mozzarella", "Parmesan", "Béchamel sauce"],
        "instructions": "Cook meat. Layer pasta, sauce, and cheese. Bake until golden."
    },
    {
        "title": "Pasta Pesto",
        "difficulty": "Easy",
        "description": "A fresh and flavorful pasta dish with basil pesto.",
        "ingredients": ["Pasta", "Basil", "Pine nuts", "Parmesan", "Garlic", "Olive oil"],
        "instructions": "Cook pasta. Blend pesto ingredients. Mix with pasta and serve."
    }]

    indian = [
    {
        "title": "Butter Chicken",
        "difficulty": "Medium",
        "description": "A creamy, spiced chicken curry with butter and tomatoes.",
        "ingredients": ["Chicken", "Tomato puree", "Cream", "Butter", "Ginger", "Garlic", "Garam masala"],
        "instructions": "Marinate chicken. Cook with spices. Add tomato puree and cream. Simmer."
    },
    {
        "title": "Chana Masala",
        "difficulty": "Easy",
        "description": "A spiced chickpea curry that is rich in flavor.",
        "ingredients": ["Chickpeas", "Onion", "Tomato", "Garlic", "Ginger", "Cumin", "Coriander"],
        "instructions": "Sauté onions and spices. Add tomatoes and chickpeas. Simmer and serve."
    },
    {
        "title": "Biryani",
        "difficulty": "Hard",
        "description": "A fragrant rice dish with spiced meat and saffron.",
        "ingredients": ["Basmati rice", "Chicken", "Yogurt", "Onions", "Spices", "Saffron"],
        "instructions": "Marinate chicken. Layer with rice and spices. Cook on low heat."
    }]

    # Chinese Recipes
    chinese = [
    {
        "title": "Kung Pao Chicken",
        "difficulty": "Medium",
        "description": "A spicy stir-fried chicken dish with peanuts and vegetables.",
        "ingredients": ["Chicken", "Bell peppers", "Peanuts", "Soy sauce", "Garlic", "Chili flakes"],
        "instructions": "Stir-fry chicken. Add veggies and sauce. Garnish with peanuts."
    },
    {
        "title": "Fried Rice",
        "difficulty": "Easy",
        "description": "A quick and flavorful rice dish with vegetables and egg.",
        "ingredients": ["Rice", "Eggs", "Carrots", "Peas", "Soy sauce", "Garlic", "Oil"],
        "instructions": "Stir-fry veggies. Add rice and eggs. Mix with soy sauce."
    },
    {
        "title": "Peking Duck",
        "difficulty": "Hard",
        "description": "A crispy roasted duck served with pancakes and hoisin sauce.",
        "ingredients": ["Duck", "Hoisin sauce", "Cucumber", "Green onions", "Pancakes"],
        "instructions": "Roast duck until crispy. Slice and serve with pancakes and hoisin sauce."
    }]

    cats = {'Italian': {'pages': italian},
            'Indian': {'pages': indian},
            'Chinese': {'pages': chinese} }

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_recipe(c, p['title'], p['difficulty'], p['description'], p['ingredients'], p['instructions'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Recipe.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_recipe(cat, title, difficulty, description, ingredients, instructions):
    p = Recipe.objects.get_or_create(category=cat, title=title)[0]
    p.difficulty=difficulty
    p.description=description
    p.ingredients=ingredients
    p.instructions=instructions
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()