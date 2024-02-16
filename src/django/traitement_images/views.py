import os
from django import forms
from django.conf import settings
from django.shortcuts import render
from .utils import align_images, animate_images, apply_greyscale, convert_to_bw, merge_images, resize_an_image
from django.core.files.storage import FileSystemStorage

class UploadForm(forms.Form):
    file_input = forms.FileField(label='Fichier à traiter :')
    

class UploadForm2(forms.Form):
    file_input_1 = forms.FileField(label='Fichier à traiter :')
    file_input_2 = forms.FileField(label='Deuxième fichier :')

class UploadForm3(forms.Form):
    images = forms.FileField(label='Fichiers à traiter :')

def home(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file_input']
            if not uploaded_file:
                return render(request, 'home_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un fichier.'})
            try:
                fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])
                old_filename = uploaded_file.name
                if fs.exists(old_filename):
                    fs.delete(old_filename)
                fs.save(old_filename, uploaded_file)
                image_url = fs.url(old_filename)
                return render(request, 'home_template.html', {'image_url': image_url})
                ##return redirect('home')
            except ValueError as e:
                # Gérer l'erreur si l'image ne peut pas être ouverte
                return error_404(request, e)
    else:
        form = UploadForm()
    
    return render(request, 'home_template.html', {'form': form})

def convert_image_bw(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file_input']
            if not uploaded_file:
                return render(request, 'convert_to_bw_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un fichier.'})
            try:
                fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])
                old_filename = uploaded_file.name
                if fs.exists(old_filename):
                    fs.delete(old_filename)
                fs.save(old_filename, uploaded_file)
                image_url = fs.url(old_filename)
                
                bw_image = convert_to_bw(fs.path(old_filename))
                # Enregistrer l'image en noir et blanc sur le système de fichiers
                bw_filename = f"bw_{old_filename}"
                if fs.exists(bw_filename):
                    fs.delete(bw_filename)
                bw_temp_file = os.path.join(settings.BASE_DIR, bw_filename)  # Chemin du fichier temporaire
                bw_image.save(bw_temp_file)  # Enregistrer l'image en noir et blanc dans le fichier temporaire

                # Enregistrer le fichier temporaire dans FileSystemStorage
                bw_image_path = fs.save(bw_filename, open(bw_temp_file, 'rb'))  # Enregistrer le fichier en utilisant le chemin temporaire

                # Supprimer le fichier temporaire
                os.remove(bw_temp_file)
                bw_image_url = fs.url(bw_image_path)
                return render(request, 'convert_to_bw_template.html', {'image_url': image_url, 'bw_image_url': bw_image_url})
            except ValueError as e:
                return error_404(request, e)
    else:
        form = UploadForm()
    
    return render(request, 'convert_to_bw_template.html', {'form': form})

def apply_grey(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file_input']
            if not uploaded_file:
                return render(request, 'apply_greyscale_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un fichier.'})
            try:
                fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])
                old_filename = uploaded_file.name
                if fs.exists(old_filename):
                    fs.delete(old_filename)
                fs.save(old_filename, uploaded_file)
                image_url = fs.url(old_filename)

                num_shades = request.POST.get('num_shades', 256)
                gray_image = apply_greyscale(fs.path(old_filename), num_shades=int(num_shades))
                gray_filename = f"gray[{num_shades}]_{old_filename}"
                if fs.exists(gray_filename):
                    fs.delete(gray_filename)
                gray_temp_file = os.path.join(settings.BASE_DIR, gray_filename)
                gray_image.save(gray_temp_file)
                gray_image_path = fs.save(gray_filename, open(gray_temp_file, 'rb'))
                os.remove(gray_temp_file)
                gray_image_url = fs.url(gray_image_path)
                return render(request, 'apply_greyscale_template.html', {'image_url': image_url, 'gray_image_url': gray_image_url})
            except ValueError as e:
                return error_404(request, e)
    
    else:
        form = UploadForm()

    return render(request, 'apply_greyscale_template.html', {'form': form})

def resize_image(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file_input']
            if not uploaded_file:
                return render(request, 'resize_image_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un fichier.'})
            try:
                fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])
                old_filename = uploaded_file.name
                if fs.exists(old_filename):
                    fs.delete(old_filename)
                fs.save(old_filename, uploaded_file)
                image_url = fs.url(old_filename)

                width = request.POST.get('width', 100)  # Utilisation de 100 comme valeur par défaut si aucune valeur n'est fournie
                height = request.POST.get('height', 100)
                new_size = (int(width), int(height))
                resized_image = resize_an_image(fs.path(old_filename), new_size)
                resized_filename = f"resized[{new_size[0]}x{new_size[1]}]_{old_filename}"
                if fs.exists(resized_filename):
                    fs.delete(resized_filename)
                resized_temp_file = os.path.join(settings.BASE_DIR, resized_filename)
                resized_image.save(resized_temp_file)
                resized_image_path = fs.save(resized_filename, open(resized_temp_file, 'rb'))
                os.remove(resized_temp_file)
                resized_image_url = fs.url(resized_image_path)
                return render(request, 'resize_image_template.html', {'image_url': image_url, 'resized_image_url': resized_image_url, 'width': width, 'height': height})
            except ValueError as e:
                return error_404(request, e)
            
    else:
        form = UploadForm()

    return render(request, 'resize_image_template.html', {'form': form})

def align_2_images_horizontal(request):
    if request.method == 'POST':
        form = UploadForm2(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file_input_1']
            uploaded_file_2 = request.FILES['file_input_2']
            if not uploaded_file:
                return render(request, 'align_images_horizontal_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un fichier.'})
            if not uploaded_file_2:
                return render(request, 'align_images_horizontal_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un deuxième fichier.'})
            try:
                fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])
                old_filename = uploaded_file.name
                if fs.exists(old_filename):
                    fs.delete(old_filename)
                fs.save(old_filename, uploaded_file)
                image_url = fs.url(old_filename)

                old_filename_2 = uploaded_file_2.name
                if fs.exists(old_filename_2):
                    fs.delete(old_filename_2)
                fs.save(old_filename_2, uploaded_file_2)
                image_url_2 = fs.url(old_filename_2)

                combined_images = align_images(fs.path(old_filename), fs.path(old_filename_2), align='horizontal')
                combined_filename = f"combined_horizontally_{old_filename}_{old_filename_2}"
                if fs.exists(combined_filename):
                    fs.delete(combined_filename)
                combined_temp_file = os.path.join(settings.BASE_DIR, combined_filename)
                combined_images.save(combined_temp_file)
                combined_image_path = fs.save(combined_filename, open(combined_temp_file, 'rb'))
                os.remove(combined_temp_file)
                combined_image_url = fs.url(combined_image_path)
                return render(request, 'align_images_horizontal_template.html', {'image_url': image_url, 'image_url_2': image_url_2, 'combined_image_url': combined_image_url})
            except ValueError as e:
                return error_404(request, e)
            
    else:
        form = UploadForm2()

    return render(request, 'align_images_horizontal_template.html', {'form': form})

def align_2_images_vertical(request):
    if request.method == 'POST':
        form = UploadForm2(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file_input_1']
            uploaded_file_2 = request.FILES['file_input_2']
            if not uploaded_file:
                return render(request, 'align_images_vertical_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un fichier.'})
            if not uploaded_file_2:
                return render(request, 'align_images_vertical_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un deuxième fichier.'})
            try:
                fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])
                old_filename = uploaded_file.name
                if fs.exists(old_filename):
                    fs.delete(old_filename)
                fs.save(old_filename, uploaded_file)
                image_url = fs.url(old_filename)

                old_filename_2 = uploaded_file_2.name
                if fs.exists(old_filename_2):
                    fs.delete(old_filename_2)
                fs.save(old_filename_2, uploaded_file_2)
                image_url_2 = fs.url(old_filename_2)

                combined_images = align_images(fs.path(old_filename), fs.path(old_filename_2), align='vertical')
                combined_filename = f"combined_vertically_{old_filename}_{old_filename_2}"
                if fs.exists(combined_filename):
                    fs.delete(combined_filename)
                combined_temp_file = os.path.join(settings.BASE_DIR, combined_filename)
                combined_images.save(combined_temp_file)
                combined_image_path = fs.save(combined_filename, open(combined_temp_file, 'rb'))
                os.remove(combined_temp_file)
                combined_image_url = fs.url(combined_image_path)
                return render(request, 'align_images_vertical_template.html', {'image_url': image_url, 'image_url_2': image_url_2, 'combined_image_url': combined_image_url})
            except ValueError as e:
                return error_404(request, e)
            
    else:
        form = UploadForm2()

    return render(request, 'align_images_vertical_template.html', {'form': form})

def merge_2_images(request):
    if request.method == 'POST':
        form = UploadForm2(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file_input_1']
            uploaded_file_2 = request.FILES['file_input_2']
            if not uploaded_file:
                return render(request, 'merge_images_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un fichier.'})
            if not uploaded_file_2:
                return render(request, 'merge_images_template.html', {'form': form, 'error_message': 'Veuillez sélectionner un deuxième fichier.'})
            try:
                fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])
                old_filename = uploaded_file.name
                if fs.exists(old_filename):
                    fs.delete(old_filename)
                fs.save(old_filename, uploaded_file)
                image_url = fs.url(old_filename)

                old_filename_2 = uploaded_file_2.name
                if fs.exists(old_filename_2):
                    fs.delete(old_filename_2)
                fs.save(old_filename_2, uploaded_file_2)
                image_url_2 = fs.url(old_filename_2)

                ratio = request.POST.get('ratio')
                position1_x = request.POST.get('position1_x')
                position1_y = request.POST.get('position1_y')
                position2_x = request.POST.get('position2_x')
                position2_y = request.POST.get('position2_y')
                ratio = float(ratio)
                position1_x = int(position1_x)
                position1_y = int(position1_y)
                position2_x = int(position2_x)
                position2_y = int(position2_y)
                merged_images = merge_images(fs.path(old_filename), fs.path(old_filename_2), ratio=ratio, position1=(position1_x, position1_y), position2=(position2_x, position2_y))
                merged_filename = f"merged_{int(float(ratio) * 100)}%_{old_filename}_{old_filename_2}"
                if fs.exists(merged_filename):
                    fs.delete(merged_filename)
                merged_temp_file = os.path.join(settings.BASE_DIR, merged_filename)
                merged_images.save(merged_temp_file)
                merged_image_path = fs.save(merged_filename, open(merged_temp_file, 'rb'))
                os.remove(merged_temp_file)
                merged_image_url = fs.url(merged_image_path)
                return render(request, 'merge_images_template.html', {'image_url': image_url, 'image_url_2': image_url_2, 'merged_image_url': merged_image_url})
            except ValueError as e:
                print(e)
                return error_404(request, e)
            
    else:
        form = UploadForm2()

    return render(request, 'merge_images_template.html', {'form': form})


def animate_2_images(request):
    if request.method == 'POST':
        form = UploadForm3(request.POST, request.FILES)
        if form.is_valid():
            animated_images_paths = []
            images_urls = []  # Initialisation de la liste pour stocker les URL des images
            for uploaded_file in request.FILES.getlist('images'):
                try:
                    fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0])
                    old_filename = uploaded_file.name
                    if fs.exists(old_filename):
                        fs.delete(old_filename)
                    fs.save(old_filename, uploaded_file)
                    image_url = fs.url(old_filename)
                    images_urls.append(image_url)  # Ajout de l'URL de l'image à la liste
                    animated_images_paths.append(fs.path(old_filename))
                except ValueError as e:
                    return error_404(request, e)

            # Appel de la fonction pour animer les images
            animated_image_url = animate_images(animated_images_paths, output_file=os.path.join(settings.STATICFILES_DIRS[0], 'animated_images.gif'), fps=24, slowdown_factor=20)

            if animated_image_url is None:
                return error_404(request, "Impossible de créer l'animation.")

            return render(request, 'animate_images_template.html', {'images_urls': images_urls, 'animated_image_url': animated_image_url})
            
    else:
        form = UploadForm3()

    return render(request, 'animate_images_template.html', {'form': form})



def error_404(request, e):
    return render(request, 'error_template.html', {'error_message': str(e)}) 
    