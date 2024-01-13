"""
crop된 영상 프레임에서 target 물체를 classification 하기 위한 모듈입니다.
"""
from utils.Inference.otx_api import OTXAPI


class BottleClassifier(OTXAPI):
    """OTX API를 상속받아 classification을 수행하는 클래스"""

    PET_BOTTLE_MODEL = {
        "model_template_path": "resources/pet_bottle_classification/template",
        "model_weight_path": "resources/pet_bottle_classification/model/model.xml",
        "model_name": "Custom_Image_Classification_EfficientNet-V2-S"
        }
    GLASS_BOTTLE_MODEL = {
        "model_template_path": "resources/glass_bottle_classification/template",
        "model_weight_path": "resources/glass_bottle_classification/model/model.xml",
        "model_name": "Custom_Image_Classification_DeiT-Tiny"
        }

    def __init__(self):
        super().__init__()
        self.current_target = None
        self.set_model_target()

    def __str__(self):
        """현재 model이 target하고 있는 물체의 이름을 리턴합니다."""
        return self.current_target

    def set_model_target(self, target="pet"):
        """model을 통해 classification하고자 하는 물체를 지정합니다."""
        if target == "pet":
            self.current_target = "pet"
            self.task = super()._init_task(
                self.PET_BOTTLE_MODEL["model_template_path"],
                self.PET_BOTTLE_MODEL["model_weight_path"],
                self.PET_BOTTLE_MODEL["model_name"]
                )
            return

        if target == "glass":
            self.current_target = "glass"
            self.task = super()._init_task(
                self.GLASS_BOTTLE_MODEL["model_template_path"],
                self.GLASS_BOTTLE_MODEL["model_weight_path"],
                self.GLASS_BOTTLE_MODEL["model_name"]
                )
            return

    def classify_bottle(self, frame) -> int:
        """ target 물체가 페트병인 경우 비닐라벨 부착여부로 2개의 클래스로 분류하고,
        target 물체가 유리병인 경우 철뚜껑 부착여부로 2개의 클래스로 분류합니다.

        return: (target 물체가 페트병인 경우) clear bottle이면 0, label bottle이면 1
        return: (target 물체가 유리병인 경우) clear bottle이면 0, lid bottle이면 1
        """
        prediction, _ = self._get_predictions(frame)
        return int(prediction[-1].get_labels()[-1].get_label().id)
