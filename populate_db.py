from main import models as main_models
from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ Check if user exists before creating
if not User.objects.filter(username='abcdef').exists():
    user_instance = User.objects.create_superuser(
        username='abcdef', 
        email='email@email.com', 
        password='abcdef'
    )
else:
    user_instance = User.objects.get(username='abcdef')

# ✅ Check if Address exists
if not main_models.Address.objects.filter(user=user_instance).exists():
    main_models.Address.objects.create(
        user=user_instance, 
        line_1="Line 1 of address", 
        line_2="Line 2 of address", 
        city="Delhi", 
        state="Delhi", 
        country="India", 
        pin_code="123456"
    )

# ✅ Add Styles if they don't exist
styles_data = [
    {"name": "Bricks", "image": "styles/bricks.jpeg", "image_model": "bricks.h5"},
    {"name": "Music", "image": "styles/music.jpg", "image_model": "music2epoch.h5"},
    {"name": "Rain Princess", "image": "styles/rain_princess.jpg", "image_model": "rain_princess.h5"},
    {"name": "Starry Night", "image": "styles/starry_night.jpeg", "image_model": "starry_night.h5"},
    {"name": "Udnie", "image": "styles/udnie.jpg", "image_model": "udnie2epoch.h5"},
]

for style in styles_data:
    main_models.Styles.objects.get_or_create(**style)

# ✅ Add Templates if they don't exist
templates_data = [
    {"name": "T-Shirt", "image": "static/templates/tshirt.png", "unit_price": "450"},
    {"name": "Shirt", "image": "static/templates/shirt.png", "unit_price": "500"},
    {"name": "Mug", "image": "static/templates/mug.png", "unit_price": "200"},
    {"name": "Pillow", "image": "static/templates/pillow.png", "unit_price": "300"},
    {"name": "Phone Cover", "image": "static/templates/phonecover.png", "unit_price": "110"},
]

for template in templates_data:
    main_models.Templates.objects.get_or_create(**template)
