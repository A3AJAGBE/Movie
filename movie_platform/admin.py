from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group


@admin.register(Genre)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('Name', 'view_movies')

    def view_movies(self, obj):
        count = obj.movie.count()

        if count <= 1:
            return f'{count} Movie'
        else:
            return f'{count} Movies'

    view_movies.short_description = "Movies"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Summary', 'Price', 'Discount', 'Image', 'get_genre', 'Link', 'Rating')
    prepopulated_fields = {'slug': ('Title',)}
    list_filter = ('Genre', 'Uploaded_on')
    search_fields = ('Title',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('Customer', 'Movie', 'Quantity', 'Complete')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('Customer', 'get_movie', 'Date_Ordered', 'Order_Code', 'Complete', 'Payment', 'Coupon')
    list_display_links = ('Customer', 'Coupon')
    search_fields = ('Customer', )
    list_filter = ('Payment', 'Complete')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('Stripe_Charge_ID', 'Customer', 'Amount', 'Timestamp',)


@admin.register(Coupon)
class Coupon(admin.ModelAdmin):
    list_display = ('Code', 'Amount')

# Customize Admin page


admin.site.site_header = 'Movierium Administrator'
admin.site.index_title = 'Admin Dashboard'
admin.site.site_title = 'Movierium'

admin.site.unregister(Group)
