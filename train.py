import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('ultralytics/cfg/models/WCAY/yolov8s_WCAY.yaml')
    model.train(data='E:/.1Deeplearning--------/Datasets/A.2025fracture/FracAtlas/FracAtlas_YOLO/cp_data.yaml',
                cache=False,
                imgsz=640,
                epochs=1,
                batch=4,
                close_mosaic=10,
                workers=4,
                device='0',
                # optimizer='SGD', # using SGD
                patience=50,
                # resume='', # last.pt path
                # amp=False, # close amp
                # fraction=0.2,
                project='runs/train',
                name='exp',
                )