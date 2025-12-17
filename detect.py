import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('runs/train/other/ssdd）ours/weights/best.pt') # select your model.pt path
    # model.predict(source='E:/.1Deeplearning--------/Datasets/NEU-DET/images/val',
    model.predict(source='dataset/images/train',
                  imgsz=640,
                  project='runs/detect',
                  name='exp',
                  save=True,
                  # conf=0.2,
                  # visualize=True # visualize model features maps
                )