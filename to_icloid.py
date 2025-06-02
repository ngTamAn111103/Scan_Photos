# Tìm ảnh chưa có giữa gg photos và icloud

# Chưa xử lý được file heic, mov -> pip3 install pillow-heif

import time
start_time = time.time() # Ghi lại thời điểm bắt đầu

import os
import shutil
import imagehash
from PIL import Image 
from pillow_heif import register_heif_opener
import cv2
import numpy as np

# Cấu hình đường dẫn
inputA = "A:/Google Photos/A"
inputB = "C:/Users/ANNGUYEN/Pictures/iCloud Photos"
output = "A:/Google Photos/Output_iCloud"

# Tạo thư mục output nếu chưa tồn tại
os.makedirs(output, exist_ok=True)

# Danh sách định dạng file hỗ trợ
# IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff','.dng','.webp']
IMAGE_EXTS = []
# VIDEO_EXTS = ['.mp4', '.avi', '.mkv', '.flv', '.wmv']
VIDEO_EXTS = ['.mov']

def compute_phash(file_path):
    """Tính perceptual hash cho ảnh hoặc video"""
    try:
        # Xử lý video - lấy frame đầu tiên
        if any(file_path.lower().endswith(ext) for ext in VIDEO_EXTS):
            cap = cv2.VideoCapture(file_path)
            ret, frame = cap.read()
            cap.release()
            if not ret:
                return None
            
            # Chuyển OpenCV BGR sang RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
        
        # Xử lý ảnh
        else:
            register_heif_opener()
            img = Image.open(file_path)
        
        # Tính perceptual hash và chuẩn hóa kích thước
        img = img.convert("L").resize((64, 64), Image.LANCZOS)
        return imagehash.phash(img)
    
    except Exception as e:
        print(f"Lỗi khi xử lý {file_path}: {str(e)}")
        return None

def collect_hashes(directory):
    """Thu thập các hash từ thư mục"""
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IMAGE_EXTS + VIDEO_EXTS:
                file_path = os.path.join(root, file)
                file_hash = compute_phash(file_path)
                if file_hash:
                    hashes[file_hash] = file_path
                    print(len(hashes))
    return hashes

def main():
    # Bước 1: Thu thập tất cả hash từ inputB
    print("Đang thu thập hash từ inputB...")
    b_hashes = collect_hashes(inputB)
    print(f"Đã thu thập {len(b_hashes)} hash từ inputB")
    
    # Bước 2: Duyệt qua inputA và kiểm tra
    print("Đang kiểm tra file trong inputA...")
    for root, _, files in os.walk(inputA):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IMAGE_EXTS + VIDEO_EXTS:
                file_path = os.path.join(root, file)
                
                # Tính hash cho file hiện tại
                current_hash = compute_phash(file_path)
                if not current_hash:
                    continue
                
                # Kiểm tra xem hashA có tồn tại trong inputB không
                found = False
                for b_hash in b_hashes:
                    # So sánh với ngưỡng sai khác cho phép
                    if current_hash - b_hash <= 5:  # Có thể điều chỉnh ngưỡng này
                        found = True
                        break
                
                # Nếu không tìm thấy trong inputB, copy sang output
                if not found:
                    dest_path = os.path.join(output, file)
                    
                    # Xử lý trùng tên file
                    counter = 1
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(file)
                        dest_path = os.path.join(output, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    shutil.copy2(file_path, dest_path)
                    print(f"Đã copy: {file} -> {dest_path}")
                    time.sleep(1)

if __name__ == "__main__":
    main()

end_time = time.time()   # Ghi lại thời điểm kết thúc
elapsed_time = end_time - start_time # Tính thời gian đã trôi qua

print(f"Thời gian thực thi: {elapsed_time:.4f} giây")


