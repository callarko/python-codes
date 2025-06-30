# MLfolder/training_script.py
import argparse
import os
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', type=str, help='Path to the training data')
    args = parser.parse_args()
    
    # Simulate training
    print("Training script is running...")
    data = np.loadtxt(args.data_path)
    print(f"Data shape: {data.shape}")
    print("Training completed.")

    # Save some output
    os.makedirs('outputs', exist_ok=True)
    with open('outputs/result.txt', 'w') as f:
        f.write("Training completed successfully.")

if __name__ == '__main__':
    main()
