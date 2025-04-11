from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.utils import timezone
import os
import tensorflow as tf
from keras import datasets, layers, models
from keras.utils import save_img 
import numpy as np
from django.contrib.auth.decorators import login_required
tf.compat.v1.enable_eager_execution()

from django.conf import settings

from main import models as main_models
from main import forms as main_forms

import cloudinary
import requests
import io
from PIL import Image
from django.contrib.auth import get_user_model
User = get_user_model()

nav_cart_limit = 3
cloudinary.config( 
    cloud_name = "djfgkkrts",
    api_key = "998392861452619",
    api_secret = "Pqdk_fjwAjLRsK17MvIziHGhnkQ"
)

def load_img(path_to_img):
    img_data = requests.get(path_to_img).content

    # ✅ Step 1: Check file format
    try:
        image = Image.open(io.BytesIO(img_data))
        print(f"Image format: {image.format}")
        if image.format not in ["JPEG", "PNG", "GIF", "BMP"]:
            raise ValueError("Unsupported image format. Must be JPEG, PNG, GIF, or BMP.")
    except Exception as e:
        print("Error loading image:", e)
        raise ValueError("Image file is corrupted or invalid.")

    # ✅ Step 2: Process image if valid
    img = tf.image.decode_jpeg(img_data, channels=3)  # ERROR LINE
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, (256, 256))
    img = img[tf.newaxis, :]
    return img

def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor.numpy(), dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return tensor

# from main.functions.functions import handle_uploaded_file
# Create your views here.
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), padding='same', input_shape=(256, 256, 3)))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(64, (3, 3), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(128, (3, 3), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
# model.add(layers.Conv2D(256, (3, 3), padding='same'))
# model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer='zeros', gamma_initializer='ones', moving_mean_initializer='zeros', moving_variance_initializer='ones'))#, beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
# model.add(Activation('relu'))
# model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(256, (3, 3), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2DTranspose(128, (3, 3), strides=(2, 2), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.Conv2DTranspose(64, (3, 3), strides=(2, 2), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.Conv2DTranspose(32, (3, 3), strides=(2, 2), padding='same'))
model.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
									beta_initializer='zeros', gamma_initializer='ones',
									moving_mean_initializer='zeros',
									moving_variance_initializer='ones'))  # , beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
model.add(layers.Activation('relu'))
model.add(layers.Conv2D(3, (3, 3), activation='tanh', padding='same'))

def uploadImage(image, path):
    # https://cloudinary.com/documentation/django_integration
    # cloudinary.uploader.upload("dog.mp4", 
    # folder = "my_folder/my_sub_folder/", 
    # public_id = "my_dog",
    # overwrite = true, 
    # notification_url = "https://mysite.example.com/notify_endpoint", 
    # resource_type = "video")
    
    # upload image to cloud
    # cloudinary.uploader.upload(request.FILES['file'])
    print("cloudinary upload 1")
    uploaded_image = cloudinary.uploader.upload(image,
        folder = path,
        overwrite = True,
        resource_type = "image"
    )
    print("cloudinary upload 2")
    image_url = uploaded_image["secure_url"]
    # image_url = uploaded_image["url"]
    print(image_url)
    return image_url

def processStyleForm(style_form_json, username):
    style_id = style_form_json['style_id']
    content_image_url = style_form_json['content_image_url']

    temp = main_models.Styles.objects.get(id = style_id)
    # now we have somehow form the final image
    # temp = CompleteShirt.objects.latest('id')
    # model.load_weights(temp.style.image_ckpt.url[1:])

    print("Index Page 1")
    model.load_weights(settings.DATA["STYLES_IMAGE_MODEL"] + temp.image_model)
    print("Index Page 2")

    image = load_img(content_image_url)
    print("Index Page 3")
    image = model(image)
    print("Index Page 4")
    image = (image+1)/2
    print("Index Page 5")
    image = tensor_to_image(image)
    print("Index Page 6")
    # saving result image at result_image_url path
    out_img = Image.fromarray(image).convert('RGB')
    result_design_io = io.BytesIO()
    out_img.save(result_design_io, format='png')
    result_design_io.seek(0)
    result_design_url = uploadImage(result_design_io, settings.DATA["RESULT_IMAGE_CLOUD"])
    # ==================================
    # result_design_url = settings.DATA["RESULT_IMAGE"]
    # save_img(result_design_url, image)
    # result_design_url = "/" + result_design_url
    # os.system("python manage.py collectstatic --no-input")
    print("Index Page 7")

    # os.system(". tf/bin/activate")
    # os.system("python3 fast-style-transfer-master/evaluate.py --checkpoint "+temp.style.image_ckpt.url[1:]+" --in-path "+temp.content.url[1:]+" --out-path media/images/123.jpg")

    styled_templates = {}
    templates = main_models.Templates.objects.all().values()
    for i in templates:
        styled_template_io = io.BytesIO()
        background = Image.open(result_design_io)
        foreground = Image.open(i['image'])
        background.paste(foreground, (0, 0), foreground)
        background.save(styled_template_io, format='png')
        styled_template_io.seek(0)
        styled_template_url = uploadImage(styled_template_io,  settings.DATA["STYLED_TEMPLATE_CLOUD"])

        styled_templates[str(i['id'])] = styled_template_url

    print("Index Page 7")
    custom_user = User.objects.filter(username = username).first()
    complete_design = {
        'user_id': custom_user.id,
        'content_image': content_image_url,
        'style_id': style_id,
        'result_design': result_design_url,
        'styled_templates': str(styled_templates)
    }

    complete_design_object = main_models.CompleteDesign.objects.create(**complete_design)
    complete_design['id'] = complete_design_object.id
    complete_design['styled_templates_list'] = styled_templates
    print("Index Page 8")
    return complete_design

def index(request):
    print(f"🔹 Request method: {request.method}")

    if request.method == "POST":
        print(f"✅ POST Data: {request.POST}")  # Print the form data

        form = main_forms.CreateStyledImageForm(request.POST, request.FILES)
        if form.is_valid():
            print("✅ Form is valid! Processing...")

            # Upload Image
            content_image_url = uploadImage(form.cleaned_data['content_image'], settings.DATA["CONTENT_IMAGE_CLOUD"])
            style_id = form.cleaned_data['style'].id if hasattr(form.cleaned_data['style'], 'id') else form.cleaned_data['style']
    
            style_form_json = {
                "style_id": style_id,
                "content_image_url": content_image_url,
            }
           

            if not request.user.is_authenticated:
                print("⚠️ User not logged in. Saving to session and redirecting...")
                request.session['style_form_json'] = style_form_json
                return HttpResponseRedirect('/auth/login?next=/')

            # Process Style Form
            try:
                complete_design = processStyleForm(style_form_json, request.user.get_username())
                request.session['complete_design'] = complete_design
                print("✅ Design Processed. Redirecting to /display/")
                return HttpResponseRedirect('/display/')
            except ValueError as e:
                print(f"⚠️ Error processing image: {e}")
                return render(request, 'main/home.html', {"error": "Failed to process image. Try again."})

        else:
            print("❌ Form is NOT valid! Errors:", form.errors)

    # Default GET request or invalid POST
    print("✅ Rendering Home Page.")
    context = {"styleshirts": main_models.Styles.objects.all()}
    get_cart = getCart(request)
    if get_cart:
        context.update(get_cart)
    
    print(f"🔹 Session Data: {request.session.items()}")
    print(f"🔹 User Authenticated? {request.user.is_authenticated}")

    if not request.user.is_authenticated:
        print("❌ User is not logged in. Redirecting...")
        return HttpResponseRedirect('/auth/login?next=/')
    
    return render(request, 'main/home.html', context)



def displayTemplates(request):
    request.session['display_active'] = True

    if not request.user.is_authenticated:
        print("⚠️ User not authenticated. Redirecting to login.")
        return HttpResponseRedirect('/auth/login?next=/display/')

    complete_design = request.session.get('complete_design', None)
    
    if not complete_design:
        print("⚠️ No design found in session. Redirecting to home.")
        if request.session.get('display_active', False):
            del request.session['display_active']
        return HttpResponseRedirect('/')

    context = {
        "content_image": complete_design.get('content_image'),
        "result_image": complete_design.get('result_design'),  # ✅ Fixed reference
        "templates": main_models.Templates.objects.all(),
        "styled_templates": complete_design.get('styled_templates_list', {})
    }

    get_cart = getCart(request)
    if get_cart:
        context = {**context, **get_cart}
    
    print("✅ Displaying templates.")
    return render(request, 'main/display.html', context)


def getCart(request, limit = nav_cart_limit):
    if not request.user.is_authenticated:
        return None

    custom_user = User.objects.filter(username = request.user.get_username())
    cart_products = main_models.Cart.objects.filter(user = custom_user[0].id, is_purchased = False)

    total_payable = 0
    for i in cart_products.values():
        total_payable += (i['quantity'] * i['unit_price'])

    context = {
        "cart_products": cart_products,
        "nav_cart_products": cart_products[:limit],
        "total_cart_payable": total_payable
    }
    return context

def cart(request):
    context = {
        "error": None
    }
    get_cart = getCart(request)
    if get_cart:
        context = {**context, **get_cart}
        return render(request, 'main/cart.html', context)

    return HttpResponseRedirect('/auth/login/?next=/cart/')

@login_required
def checkout(request):
    promocode = None
    discount = None
    context = {
        "customuser": User.objects.filter(username = request.user.get_username())[0],
        "promocode": promocode,
        "discount": discount
    }
    get_cart = getCart(request)
    if get_cart:
        context = {**context, **get_cart}
    return render(request, 'main/checkout.html', context)

def addRemoveCart(request):
    if request.method == "POST":
        if "add-to-cart" in request.POST:
            user = User.objects.filter(username = request.user.get_username())
            complete_design = request.session.get('complete_design')
            template = main_models.Templates.objects.get(id = request.POST['template_id'])
            cart_object = {
                "user_id": user[0].id,
                "is_purchased": False,
                "complete_design_id": complete_design['id'],
                "template_id": template.id,
                "styled_template_url": request.POST['styled_template_url'],
                "quantity": request.POST['quantity'],
                "unit_price": template.unit_price
            }
            cart_object["added_at"] = timezone.now()
            cart_object["last_updated_at"] = timezone.now()
            cart_object = main_models.Cart.objects.create(**cart_object)
            return HttpResponse(str(cart_object.id))
        elif "remove-from-cart" in request.POST:
            try:
                cart_object = main_models.Cart.objects.get(id = request.POST['cart_object_id'])
                cart_object.delete()
                return HttpResponse("success")
            except:
                return HttpResponse("fail")
    # response = render(request, template_name)
    # response.status_code = 404
    # return response
    return HttpResponseNotFound("hello")

def updateProductQuantity(request):
    if request.method == "POST":
        product_list_len = int(request.POST['product_list_len'])
        for i in range(product_list_len):
            cartId = request.POST['product_list[{}][0]'.format(i)]
            quantity = request.POST['product_list[{}][1]'.format(i)]
            print(main_models.Cart.objects.get(id = cartId).quantity, end = " ")
            product = main_models.Cart.objects.get(id = cartId)
            if int(quantity) == 0:
                product.delete()
            else:
                product.quantity = quantity
                product.last_updated_at = timezone.now()
                product.save(update_fields=['quantity', 'last_updated_at'])
                print(main_models.Cart.objects.get(id = cartId).quantity, end = " update ")
                print(quantity)
        return HttpResponse("success")
        # return HttpResponse("fail")
    return HttpResponseNotFound("hello")