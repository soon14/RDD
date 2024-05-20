from ultralytics import YOLO
import os
<<<<<<< HEAD
from ultralytics.utils.autobatch import autobatch
import torch, gc
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["TORCH_USE_CUDA_DSA"] = "1"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:4096"
if __name__ == '__main__':
    #Create a new YOLO model from scratch
    #model = YOLO(r'C:\Users\user\yolov8_rail\ultralytics\runs\detect\train12\weights\best.pt')
    gc.collect()
    torch.cuda.empty_cache()
    # Load a pretrained YOLO model (recommended for training)
    #model = YOLO('yolov8n.pt') #학습용모델
   
   
    # test이미지 뽑기
    model = YOLO('ultralytics/runs/detect/train12/weights/best.pt') # 베스트모델
    results = model(r'E:\urban_datasets\validation\images', conf=0.5, save=True,line_thickness =3, show_conf=False, show_labels=True)
   
    memory_allocated=torch.cuda.memory_allocated() # 현 시점에서 할당된 메모리
    print(memory_allocated)
    
    #memory_summary=torch.cuda.memory_summary() # 메모리 요약
    #print(memory_summary)


    # Train the model using the 'coco128.yaml' dataset for 3 epochs
    #results = model.train(data='data.yaml', epochs=100, patience = 10)

    # Evaluate the model's performance on the validation set
    # results = model.val()
=======
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
if __name__ == '__main__':
    # Create a new YOLO model from scratch
    model = YOLO(r'C:\Users\user\yolov8_rail\ultralytics\runs\detect\train12\weights\best.pt')

    # Load a pretrained YOLO model (recommended for training)
    #model = YOLO('yolov8n.pt')

    # Train the model using the 'coco128.yaml' dataset for 3 epochs
    #results = model.train(data='data.yaml', epochs=10000, patience = 50)

    # Evaluate the model's performance on the validation set
    results = model.val()
>>>>>>> 31180ee25a47f1ef4550332a081df6a707f009a2

    # Perform object detection on an image using the model
    #results = model('https://ultralytics.com/images/bus.jpg')

    # Export the model to ONNX format
<<<<<<< HEAD
    # success = model.export(format='onnx') 
=======
    success = model.export(format='onnx')
>>>>>>> 31180ee25a47f1ef4550332a081df6a707f009a2
    
    
    '''predict
    from ultralytics import YOLO
import cv2
model = YOLO("yolov8s.pt") # 원하는 크기 모델 입력(n ~ x)

result = model.predict("./test.png", save=True, conf=0.5)
plots = result[0].plot()
cv2.imshow("plot", plots)
cv2.waitKey(0)
<<<<<<< HEAD
cv2.destroyAllWindows()'''

C:\Users\user\yolov8_rail\ultralytics\runs\detect
=======
cv2.destroyAllWindows()'''
>>>>>>> 31180ee25a47f1ef4550332a081df6a707f009a2
