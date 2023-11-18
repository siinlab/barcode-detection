import os

def create_txt_for_images(image_folder, txt_folder):
    # Create the new folder for text files if it doesn't exist
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    # Loop through all files in the image folder
    for file in os.listdir(image_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            # Create a corresponding .txt file in the txt_folder
            base_name = os.path.splitext(file)[0]
            txt_file_path = os.path.join(txt_folder, base_name + '.txt')
            
            # Create an empty text file
            with open(txt_file_path, 'w') as txt_file:
                pass  # Nothing is written to the file, it remains empty

# Example usage
image_folder = 'C:/Users/User/Desktop/SiinLab/test dataset/images' 
txt_folder = 'C:/Users/User/Desktop/SiinLab/test dataset/labels'      # Replace with your desired txt folder path

create_txt_for_images(image_folder, txt_folder)
