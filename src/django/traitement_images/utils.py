from PIL import Image
from matplotlib import pyplot as plt

def open_image(image_path):
    try:
        img = Image.open(image_path)
        return img
    except Exception as e:
        raise ValueError(f"Erreur lors de l'ouverture de l'image : {str(e)}")

img_path = '../assets/images/Lenna.png'

img = open_image(img_path)

plt.imshow(img)
plt.show()

def convert_to_bw(image_path):
    pass

def apply_grayscale(image_path):
    pass

def resize_image(image_path, new_size):
    pass

def align_images(image_path1, image_path2):
    pass

def merge_images(image_path1, image_path2):
    pass

def animate_images(image_paths, output_path):
    pass