# Stylestore

### Problem Statement

- The clothes are much more than an item of apparel these days. The clothes a person wears reveals a lot about them. Subcounsciously our confidence levels are -associated with how we look.  
- All people have different taste in fashion depending upon on their personal outlook of how their clothes suit their shape, size, age and the amount of confidence it gives them.
- Keeping this in mind we propose to make a easy to use web based platform where we give total control to the users so they can design their merchandise with the content and style they want.

### Proposed Solution
- We propose a neural style transfer-based e-commerce web application which provides a variety of personalised items like mobile covers, mugs, t-shirts made using a combination of the content and style provided by the user.
- We’ll provide a visual estimate of how the items would look on using different styles and content given by the user
- Users can order the items they like.

![stylestore_finalvid](https://user-images.githubusercontent.com/42407286/126860339-0508b0aa-f3ed-4d69-83b5-b07b397ee394.gif)

### Solution Deep-Dive

#### Neural style transfer 
- It is an optimization technique used to take two images, content image and style reference image, blend them together such that output image look like the content image, but “painted” in the style of the style image.
- There are two loss functions, one that describes how different the content of two images are (Content Loss) and one that describes the difference between the two images in terms of their style (Style Loss). We try to minimize the LContent distance with the content image and LStyle with the style image.

In addition to user uploading his own style image we’ll also provide a list of styles to the user. The advantage of this is we can train image to image translation models to produce the final image for that particular style hence our output process would speedup and processing power required would decrease.

![image](https://user-images.githubusercontent.com/42407286/127613897-624bf65c-f378-4f35-8042-7ad7bf1cf84f.png)

### Impact
- We are trying to create a better experience for the user where we show items that are according to their taste and needs which would hopefully instill a buying behaviour in them.
- Judging from the success of various image to image translation based  products like filters on social media apps, faceapp, photo-booth on iphone, we can safely say that this product have all the ingredients to be a commercial success.
- Customers ordering personalized merchandise that make them feel confident about themselves will have a positive impact on them.
- With customized ordering in-house manufacturing will thrive.

### Steps to initialise database
```python manage.py makemigrations```  
```python manage.py migrate```  
```python manage.py shell```  
```
from main import models as main_models
from django.contrib.auth.models import User
User.objects.create_superuser(username='abcdef', email='email@email.com', password='abcdef')
main_models.Address.objects.create(**{"line_1": "Line 1 of address", "line_2": "Line 2 of address", "city": "Delhi", "state": "Delhi", "country": "India", "pin_code": "123456"})
main_models.CustomUser.objects.create(**{"username": "abcdef", "firstname": "ABC", "lastname": "DEF", "phone_number": "9876543210", "address_id": 1, "gender": 'm'})

main_models.Styles.objects.create(**{"name": "Bricks", "image": "styles/bricks.jpeg", "image_model": "bricks.h5"})
main_models.Styles.objects.create(**{"name": "Music", "image": "styles/music.jpg", "image_model": "music2epoch.h5"})
main_models.Styles.objects.create(**{"name": "Rain Princess", "image": "styles/rain_princess.jpg", "image_model": "rain_princess.h5"})
main_models.Styles.objects.create(**{"name": "Starry Night", "image": "styles/starry_night.jpeg", "image_model": "starry_night.h5"})
main_models.Styles.objects.create(**{"name": "Udnie", "image": "styles/udnie.jpg", "image_model": "udnie2epoch.h5"})

main_models.Templates.objects.create(**{"name": "T-Shirt", "image": "static/templates/tshirt.png", "unit_price": "450"})
main_models.Templates.objects.create(**{"name": "Shirt", "image": "static/templates/shirt.png", "unit_price": "500"})
main_models.Templates.objects.create(**{"name": "Mug", "image": "static/templates/mug.png", "unit_price": "200"})
main_models.Templates.objects.create(**{"name": "Pillow", "image": "static/templates/pillow.png", "unit_price": "300"})
main_models.Templates.objects.create(**{"name": "Phone Cover", "image": "static/templates/phonecover.png", "unit_price": "110"})
quit()
```

### Steps to start app
```python manage.py collectstatic --no-input```  
```python manage.py runserver```  



