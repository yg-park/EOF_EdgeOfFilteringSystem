# import libs
# prepare dataset
# build model
# compile model
# review model
# train model
# evaluation model
# save model


import torch
from PIL import Image

# YOLOv5 모델 불러오기
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 이미지 불러오기
image_path = 'data/test_image.jpeg'
img = Image.open(image_path)

# 객체 검출 수행
results = model(img)

# 결과 출력
results.show()  # 결과 시각화
print(results.xyxy[0])  # 감지된 객체 정보 출력




"""
import cv2
import torch
from torchvision import transforms
from PIL import Image

# YOLO 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()

# 이미지 로드 및 전처리
# image_path = 'data/testtest.jpeg'
image_path = 'data/insadong.jpg'
# image_path = 'data/test_image.jpeg'
img = cv2.imread(image_path)
# width, height = 640, 480
# img = cv2.resize(img, (width, height))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV로 읽은 이미지를 RGB로 변환
transform = transforms.Compose([transforms.ToPILImage(), transforms.Resize(640)])
temp_img = transform(img)

# 객체 감지
results = model(temp_img)

# 사람 객체 검출
for detection in results.xyxy[0]:
    if int(detection[5]) == 0:  # COCO dataset에서 사람은 클래스 0에 해당
        confidence = float(detection[4])
        if confidence > 0.5:  # 임계값 조정 가능
            box = detection[:4].cpu().numpy().astype(int)
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
            cv2.putText(img, f'Person {confidence:.2f}', (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# 결과 이미지 출력
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) # PIL 이미지를 OpenCV 형식으로 변환
# width, height = 640, 480
# img = cv2.resize(img, (width, height))
cv2.imshow('YOLO Object Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""


