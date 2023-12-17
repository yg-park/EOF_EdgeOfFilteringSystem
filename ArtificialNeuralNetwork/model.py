import torch
import torch.nn as nn
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
import cv2


class bottle_classifier:
    """
    desc: 추론에 사용될 모델의 원형을 선언하고, 카메라를 통해 찍은 영상을 전처리할 transforms의 형태를 초기화합니다. 
    param1: 모델의 가중치가 저장된 .pth 파일의 경로를 생성자 매개변수로 받습니다.
    """
    def __init__(self, pth_PATH): 
        self.model = self._init_model(pth_PATH)
        self.data_transforms = transforms.Compose([
            transforms.ToPILImage(), # opencv로 이미지 읽어서 돌릴꺼면 pil 이미지로 한번 변환해줘야함
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(), 
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
        self.class_name = ['nl_bottle', 'yl_bottle']

    """
    desc: 모델의 형태를 초기화 하고, pretrained 된 가중치가 담긴 파일을 load 한 뒤, 모델을 추론모드로 전환합니다.
    """
    def _init_model(self, pth_PATH):
        model = models.resnet18(weights=ResNet18_Weights.DEFAULT)
        num_features = model.fc.in_features
        model.fc = nn.Linear(num_features, 2)

        model.load_state_dict(torch.load(pth_PATH))
        model.eval() # 추론모드로 전환
        return model

    """
    desc: OpenCV 함수를 통해 입력된 이미지(numpy array자료형)를 모델에 넣고 추론하여 결과를 출력합니다.
    """
    def classify(self, input_cv2_frame):
        input_cv2_frame = cv2.cvtColor(input_cv2_frame, cv2.COLOR_BGR2RGB)
        trans_cv2_frame = self.data_transforms(input_cv2_frame)
        
        with torch.no_grad():
            outputs = self.model(trans_cv2_frame.unsqueeze(0)) # 모델은 batch 디멘션이 포함된 4D 형태의 인풋을 기대하고 있으므로 3D 단일 이미지를 4D로 증강
            _, predicts = torch.max(outputs, 1)

        return self.class_name[predicts[0]] # 'nl_bottle' 또는 'yl_bottle'
        



PATH = './eof_bottle_classification_model.pth'
eof_model = bottle_classifier(PATH)

test_img = cv2.imread("test_input4.jpg")
result = eof_model.classify(test_img)

print(f"추론결과: {result}")

