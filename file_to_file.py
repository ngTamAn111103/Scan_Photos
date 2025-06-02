# Lấy tất cả ảnh và video trong 1 root nhiều con ra 1 folder
# input_directory = "C:\\\\Users\\\\ANNGUYEN\\\\Downloads\\\\PHOTOS"  # Ví dụ: "C:\\\\Users\\\\YourUser\\\\Videos"
#     output_directory = "A:\\\\Google Photos\\\\A"   # Ví dụ: "C:\\\\Users\\\\YourUser\\\\MovedVideos"

import os
import shutil

def move_video_files(input_dir, output_dir, extensions=('.mov', '.mp4', '.avi', '.mkv', '.flv','.jpg','.dng','.heic','.png','.webp','.jpeg')):
    os.makedirs(output_dir, exist_ok=True)
    
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith(extensions):
                src_path = os.path.join(root, filename)
                
                # Tạo tên file duy nhất trong output_dir
                base_name, ext = os.path.splitext(filename)
                dest_path = os.path.join(output_dir, filename)
                counter = 1
                
                while os.path.exists(dest_path):
                    new_name = f"{base_name}_{counter}{ext}"
                    dest_path = os.path.join(output_dir, new_name)
                    counter += 1
                
                shutil.move(src_path, dest_path)
                print(f"Đã di chuyển: {src_path} -> {dest_path}")

# Sử dụng
input_path = "A:\\Google Photos\\PHOTOS"  # Thay thế bằng đường dẫn thực
output_path = "A:\\Google Photos\\A"  # Thay thế bằng đường dẫn thực

move_video_files(input_path, output_path)