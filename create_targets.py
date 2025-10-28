#!/usr/bin/env python3
import json
import base64
import cv2
import numpy as np
import os
from pathlib import Path
import argparse
import sys

def create_mind_file(image_paths, output_file="targets.mind", max_size=512, quality=85):
    targets_data = {"version": "1.0", "targets": []}

    for i, image_path in enumerate(image_paths):
        p = Path(image_path)
        if not p.exists():
            print(f"❌ Không tìm thấy file {image_path}", file=sys.stderr)
            continue

        print(f"🔮 Đang xử lý {image_path}...")
        img = cv2.imread(str(p))
        if img is None:
            print(f"❌ Không thể đọc file ảnh {image_path}", file=sys.stderr)
            continue

        height, width = img.shape[:2]
        if max(height, width) > max_size:
            scale = max_size / max(height, width)
            new_w = int(width * scale)
            new_h = int(height * scale)
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        try:
            _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])
        except Exception as e:
            print(f"❌ Lỗi khi encode ảnh {image_path}: {e}", file=sys.stderr)
            continue

        img_base64 = base64.b64encode(buffer).decode('utf-8')

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
        print(f"✅ Đã thêm target {i}: {p.name}")

    if not targets_data["targets"]:
        print("❌ Không có target hợp lệ để ghi file.", file=sys.stderr)
        return False

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(targets_data, f, ensure_ascii=False, indent=2)
        print(f"\n🎉 ĐÃ TẠO THÀNH CÔNG: {output_file}")
        print(f"📁 Số lượng targets: {len(targets_data['targets'])}")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi ghi file {output_file}: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Tạo file targets.mind từ các ảnh target")
    parser.add_argument('inputs', nargs='*', help='Danh sách file ảnh hoặc thư mục chứa ảnh. Nếu để trống, tìm *.jpg, *.png trong cwd.')
    parser.add_argument('-o', '--output', default='targets.mind', help='Tên file .mind đầu ra')
    args = parser.parse_args()

    images = []
    if not args.inputs:
        # tìm ảnh trong thư mục hiện tại
        for ext in ('*.jpg','*.jpeg','*.png'):
            images.extend([str(p) for p in Path('.').glob(ext)])
    else:
        for it in args.inputs:
            p = Path(it)
            if p.is_dir():
                for ext in ('*.jpg','*.jpeg','*.png'):
                    images.extend([str(x) for x in p.glob(ext)])
            elif p.is_file():
                images.append(str(p))

    # loại bỏ trùng và kiểm tra tồn tại
    images = [str(Path(x)) for x in dict.fromkeys(images) if Path(x).exists()]

    if not images:
        print("❌ Không tìm thấy file ảnh nào! Hãy đặt ảnh vào cùng thư mục hoặc truyền đường dẫn vào.", file=sys.stderr)
        return

    print(f"📸 Tìm thấy {len(images)} ảnh target")
    create_mind_file(images, output_file=args.output)

if __name__ == "__main__":
    main()
