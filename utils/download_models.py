#!/usr/bin/env python3
"""
Download pre-trained models for object detection
Downloads TFLite models optimized for Coral USB Accelerator
"""

import os
import urllib.request
import sys


def download_file(url, destination):
    """Download a file with progress indication"""
    print(f"Downloading {os.path.basename(destination)}...")
    
    try:
        def progress_hook(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\r  Progress: {percent}%")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, destination, progress_hook)
        print("\n  Done!")
        return True
    except Exception as e:
        print(f"\n  Error: {e}")
        return False


def main():
    """Download required model files"""
    print("=" * 60)
    print("Downloading Object Detection Models for Coral USB Accelerator")
    print("=" * 60)
    print()
    
    # Create models directory
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Model files to download
    files = {
        'ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite': 
            'https://github.com/google-coral/test_data/raw/master/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite',
        'coco_labels.txt':
            'https://github.com/google-coral/test_data/raw/master/coco_labels.txt'
    }
    
    success_count = 0
    
    for filename, url in files.items():
        destination = os.path.join(models_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(destination):
            print(f"✓ {filename} already exists, skipping...")
            success_count += 1
            continue
        
        # Download file
        if download_file(url, destination):
            success_count += 1
        else:
            print(f"✗ Failed to download {filename}")
    
    print()
    print("=" * 60)
    print(f"Downloaded {success_count}/{len(files)} files")
    
    if success_count == len(files):
        print("All models downloaded successfully!")
        print(f"Models saved to: {os.path.abspath(models_dir)}")
    else:
        print("Some downloads failed. Please check your internet connection.")
        return 1
    
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
