import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    # model = YOLO('runs/train/other/DX/v8s/weights/best.pt')
    model = YOLO('runs/train/v5m/weights/best.pt')
    model.val(data='../Datasets/FracAtlas/cp_data.yaml',
              split='val',
              imgsz=640,
              batch=32,
              # rect=False,
              # save_json=True, # if you need to cal coco metrice
              project='runs/val',
              name='exp',
              )