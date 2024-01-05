"""
영상 프레임 속 페트병의 비닐라벨 부착여부를 판별하는 모듈입니다.
"""
from Inference.otx_api import OTXAPI


class PetBottleClassifier(OTXAPI):
    """OTX API를 통해 페트병 라벨 부착여부 classification을 수행하는 클래스"""
    model_template_path = "resources/pet_bottle_classification/template"
    model_weight_path = "resources/pet_bottle_classification/model/model.xml"
    model_name = "Custom_Image_Classification_EfficientNet-V2-S"

    def classify_pet_bottle(self, frame) -> int:
        """ 비닐 라벨이 제거된 페트병이면 0을 리턴하고,
            비닐라벨이 제거되지 않은 페트병이면 1을 리턴한다.
            frame: 웹캠으로부터 얻은 영상
        """
        prediction, _ = self._get_predictions(frame)
        return int(prediction[-1].get_labels()[-1].get_label().id)
