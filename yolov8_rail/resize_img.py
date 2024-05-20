from PIL import Image
import os

def resize_images_in_directory(input_directory, output_directory, new_width=640, new_height=640):
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        input_filepath = os.path.join(input_directory, filename)
        output_filepath = os.path.join(output_directory, filename)
        if os.path.isfile(input_filepath):
            try:
                img = Image.open(input_filepath)
                img = img.resize((new_width, new_height))
                img.save(output_filepath)
                print(f"Resized {filename} to {new_width}x{new_height} and saved to {output_directory}")
            except Exception as e:
                print(f"Error resizing {filename}: {e}")

input_directory_path = r"E:\rail\data\Validation\RealData\NormalRe"
output_directory_path = r"E:\rail\data\Validation\RealData\Normal640"

# 640x640으로 resize
resize_images_in_directory(input_directory_path, output_directory_path)
