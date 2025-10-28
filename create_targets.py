import json
import base64
import cv2
import numpy as np
import os
from pathlib import Path

def create_mind_file(image_paths, output_file="targets.mind"):
    """
    Tạo file targets.mind từ các ảnh target
    """
    
    targets_data = {
        "version": "1.0",
        "targets": []
    }
    
    for i, image_path in enumerate(image_paths):
        if not os.path.exists(image_path):
            print(f"❌ Lỗi: Không tìm thấy file {image_path}")
            continue
            
        print(f"🔮 Đang xử lý ảnh {image_path}...")
        
        # Đọc và xử lý ảnh
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Không thể đọc file ảnh {image_path}")
            continue
            
        # Resize ảnh để tối ưu
        height, width = img.shape[:2]
        max_size = 512
        if max(height, width) > max_size:
            scale = max_size / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height))
        
        # Chuyển đổi ảnh sang base64
        _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 85])
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Tạo data cho target
        target_data = {
            "id": i,
            "name": f"target-{i}",
            "image": f"data:image/jpeg;base64,{img_base64}",
            "width": img.shape[1],
            "height": img.shape[0],
            "type": "image",
            "active": True
        }
        
        targets_data["targets"].append(target_data)
        print(f"✅ Đã thêm target {i}: {os.path.basename(image_path)}")
    
    # Ghi file .mind
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(targets_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 ĐÃ TẠO THÀNH CÔNG: {output_file}")
    print(f"📁 Số lượng targets: {len(targets_data['targets'])}")

def main():
    print("🎯 BẮT ĐẦU TẠO FILE TARGETS.MIND")
    print("=" * 50)
    
    # DANH SÁCH ẢNH TARGET CỦA BẠN
    # THAY ĐỔI các đường dẫn này thành ảnh thực tế của bạn
    image_files = [
        "target1.jpg",    # Thay bằng ảnh target thứ nhất của bạn
        "target2.jpg",    # Thay bằng ảnh target thứ hai của bạn
        "target3.jpg",    # Thêm nếu có
        "target4.jpg"     # Thêm nếu có
    ]
    
    # Chỉ giữ lại các file thực sự tồn tại
    existing_images = [img for img in image_files if os.path.exists(img)]
    
    if not existing_images:
        print("❌ Không tìm thấy file ảnh nào!")
        print("Hãy đảm bảo các file ảnh nằm trong cùng thư mục với script này")
        return
    
    print(f"📸 Tìm thấy {len(existing_images)} ảnh target")
    
    # Tạo file targets.mind
    create_mind_file(existing_images)

if __name__ == "__main__":
    main()