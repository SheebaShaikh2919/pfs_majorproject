from django.contrib import admin
from main.models import (
    Address,
    Coupon,
    Styles,
    Templates,
    CustomUser,
    Order,
    CompleteDesign,
    Cart,
)

admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(Styles)
admin.site.register(Templates)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(CompleteDesign)
admin.site.register(Cart)
