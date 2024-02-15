from PIL import Image, ImageOps
from django.conf import settings
import numpy as np

def open_image(image_path):
    img = Image.open(image_path)
    return img

def convert_to_bw(image_path):
    img = Image.open(image_path)
    bw_img = img.convert('L')    
    return bw_img

def apply_greyscale(image_path, num_shades=256):
    # Ouvre l'image
    img = Image.open(image_path)
    # Convertit l'image en niveaux de gris
    img_gray = ImageOps.grayscale(img)
    # Convertit l'image en tableau numpy
    img_array = np.array(img_gray)
    # Calcule l'intervalle entre les niveaux de gris
    interval = 256 / num_shades
    # Réduit le nombre de nuances de gris
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            img_array[i, j] = int(img_array[i, j] / interval) * interval
    # Convertit le tableau numpy en image PIL
    img_result = Image.fromarray(img_array)
    return img_result

def resize_an_image(image_path, new_size):
    img = Image.open(image_path)
    img_resized = img.resize(new_size)
    return img_resized

def align_images(image_path1, image_path2, align='horizontal'):
    img_1 = Image.open(image_path1)
    img_2 = Image.open(image_path2)

    # Si l'alignement est horizontal, redimensionnez les images pour avoir la même hauteur
    if align == 'horizontal':
        width1, height1 = img_1.size
        width2, height2 = img_2.size
        new_height = max(height1, height2)
        img_1 = img_1.resize((int(width1 * (new_height / height1)), new_height))
        img_2 = img_2.resize((int(width2 * (new_height / height2)), new_height))

    # Si l'alignement est vertical, redimensionnez les images pour avoir la même largeur
    elif align == 'vertical':
        width1, height1 = img_1.size
        width2, height2 = img_2.size
        new_width = max(width1, width2)
        img_1 = img_1.resize((new_width, int(height1 * (new_width / width1))))
        img_2 = img_2.resize((new_width, int(height2 * (new_width / width2))))

    # Alignement horizontal par défaut
    else:
        width1, height1 = img_1.size
        width2, height2 = img_2.size
        new_height = max(height1, height2)
        img_1 = img_1.resize((int(width1 * (new_height / height1)), new_height))
        img_2 = img_2.resize((int(width2 * (new_height / height2)), new_height))

    # Créer une image vierge avec la taille combinée des deux images
    if align == 'horizontal':
        combined_image = Image.new('RGB', (img_1.width + img_2.width, img_1.height))
        combined_image.paste(img_1, (0, 0))
        combined_image.paste(img_2, (img_1.width, 0))
    elif align == 'vertical':
        combined_image = Image.new('RGB', (img_1.width, img_1.height + img_2.height))
        combined_image.paste(img_1, (0, 0))
        combined_image.paste(img_2, (0, img_1.height))

    return combined_image

def merge_images(image_path1, image_path2, ratio):
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # Redimensionner les images pour qu'elles aient la même taille si nécessaire
    if image1.size != image2.size:
        min_width = min(image1.size[0], image2.size[0])
        min_height = min(image1.size[1], image2.size[1])
        target_size = (min_width, min_height)
        image1 = image1.resize(target_size)
        image2 = image2.resize(target_size)

    if image1.mode != image2.mode:
        image2 = image2.convert(image1.mode)

    # Fusionner les images
    blended_image = Image.blend(image1, image2, ratio)
    return blended_image
    

def animate_images(image_paths, output_file, fps=24, slowdown_factor=20):
    images = [Image.open(image_path) for image_path in image_paths]

    # Trouver les dimensions maximales parmi toutes les images
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)

    # Redimensionner toutes les images pour qu'elles correspondent à la plus grande dimension
    resized_images = [img.resize((max_width, max_height)) for img in images]

    # Ralentir l'animation en ajustant la durée
    duration = int(1000 / (fps / slowdown_factor))

    resized_images[0].save(output_file, format='GIF', save_all=True, append_images=resized_images[1:], loop=0, duration=duration)
    return output_file
