import os


def delete_content(folder_path):
    print("delete_content started")
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Iterate over each file and delete it
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    print("All files have been deleted.")

# def clean():
#   images = glob.glob("images/*.png")
#   for image in images:
#   os.remove(image)

# this would work aswell
