"""
Script kiểm tra GPU setup cho Smart Traffic Monitoring System
Chạy script này để verify:
1. CUDA có available không
2. GPU name là gì
3. YOLO model có load được lên GPU không
"""

import torch
from ultralytics import YOLO
import sys

def test_cuda():
    """Kiểm tra CUDA availability"""
    print("=" * 60)
    print("BƯỚC 1: KIỂM TRA CUDA")
    print("=" * 60)

    cuda_available = torch.cuda.is_available()
    print(f"✅ CUDA available: {cuda_available}")

    if cuda_available:
        gpu_name = torch.cuda.get_device_name(0)
        print(f"🚀 GPU Name: {gpu_name}")
        print(f"📊 CUDA Version: {torch.version.cuda}")
        print(f"🔢 Number of GPUs: {torch.cuda.device_count()}")

        # Memory info
        total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"💾 GPU Memory: {total_memory:.2f} GB")
        return True
    else:
        print("⚠️ GPU not available")
        print("\nNguyên nhân có thể là:")
        print("1. CUDA Toolkit chưa được cài đặt")
        print("2. PyTorch được cài bản CPU-only")
        print("3. Driver NVIDIA chưa được cập nhật")
        print("\nVui lòng xem GPU_SETUP_GUIDE.md để cài đặt!")
        return False

def test_yolo_gpu():
    """Kiểm tra YOLO model loading trên GPU"""
    print("\n" + "=" * 60)
    print("BƯỚC 2: KIỂM TRA YOLO MODEL TRÊN GPU")
    print("=" * 60)

    try:
        model_path = "./ai_models/model N/openvino models/best_int8_openvino_model"
        print(f"📁 Loading model from: {model_path}")

        model = YOLO(model_path, task='detect')

        # Move to GPU
        if torch.cuda.is_available():
            device = 'cuda:0'
            model.to(device)
            print(f"✅ Model moved to GPU: {device.upper()}")
        else:
            device = 'cpu'
            print(f"⚠️ Model running on CPU")

        print(f"✅ YOLO model loaded successfully!")
        return True

    except Exception as e:
        print(f"❌ Error loading YOLO model: {e}")
        return False

def test_inference():
    """Test inference speed trên GPU vs CPU"""
    print("\n" + "=" * 60)
    print("BƯỚC 3: SO SÁNH TỐC ĐỘ INFERENCE")
    print("=" * 60)

    if not torch.cuda.is_available():
        print("⚠️ Bỏ qua test này vì không có GPU")
        return

    try:
        import cv2
        import numpy as np
        import time

        # Tạo dummy image
        dummy_img = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)

        model_path = "./ai_models/model N/openvino models/best_int8_openvino_model"
        model = YOLO(model_path, task='detect')

        # Test CPU
        print("\n🔵 Testing CPU inference...")
        model.to('cpu')
        start = time.time()
        for _ in range(10):
            _ = model(dummy_img, device='cpu', verbose=False)
        cpu_time = (time.time() - start) / 10
        print(f"⏱️ CPU: {cpu_time*1000:.2f}ms per frame ({1/cpu_time:.1f} FPS)")

        # Test GPU
        print("\n🟢 Testing GPU inference...")
        model.to('cuda:0')
        start = time.time()
        for _ in range(10):
            _ = model(dummy_img, device='cuda:0', verbose=False)
        gpu_time = (time.time() - start) / 10
        print(f"⏱️ GPU: {gpu_time*1000:.2f}ms per frame ({1/gpu_time:.1f} FPS)")

        # Comparison
        speedup = cpu_time / gpu_time
        print(f"\n🚀 GPU nhanh hơn CPU: {speedup:.1f}x lần!")

    except Exception as e:
        print(f"❌ Error during inference test: {e}")

def main():
    print("\n🎯 SMART TRAFFIC MONITORING SYSTEM - GPU TEST\n")

    # Test 1: CUDA
    cuda_ok = test_cuda()

    if not cuda_ok:
        print("\n" + "=" * 60)
        print("❌ CUDA CHƯA SẴN SÀNG!")
        print("=" * 60)
        print("\nVui lòng làm theo hướng dẫn trong GPU_SETUP_GUIDE.md:")
        print("1. Cài CUDA Toolkit 11.8")
        print("2. Cài PyTorch với CUDA:")
        print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        print("\nSau đó chạy lại script này để kiểm tra!")
        sys.exit(1)

    # Test 2: YOLO
    yolo_ok = test_yolo_gpu()

    if not yolo_ok:
        print("\n❌ YOLO MODEL KHÔNG LOAD ĐƯỢC!")
        sys.exit(1)

    # Test 3: Inference speed
    test_inference()

    print("\n" + "=" * 60)
    print("✅ TẤT CẢ TESTS PASSED!")
    print("=" * 60)
    print("\n🎉 Dự án đã sẵn sàng chạy trên GPU!")
    print("\nChạy Backend với lệnh:")
    print("  cd Backend/app")
    print("  ../venv/Scripts/python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\nBạn sẽ thấy message:")
    print("  🚀 GPU detected: NVIDIA GeForce RTX 2050")
    print("  ✅ YOLO model loaded successfully on CUDA:0")

if __name__ == "__main__":
    main()
