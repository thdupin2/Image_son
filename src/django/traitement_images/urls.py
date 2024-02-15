from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('convert_to_bw/', views.convert_image_bw, name='convert-to-bw'),
    path('apply_grey/', views.apply_grey, name='apply-grey'),
    path('resizing/', views.resize_image, name='resize-image'),
    path('aligning_horizontal/', views.align_2_images_horizontal, name='align-images-horizontal'),
    path('aligning_vertical/', views.align_2_images_vertical, name='align-images-vertical'),
    path('merging/', views.merge_2_images, name='merge-images'),
    path('animation/', views.animate_2_images, name='animate-images'),
    path('error/', views.error_404, name='error_404')
]