"""
영상 프레임에서 target 물체를 detection하기 위한 모듈입니다.
"""
from utils.Inference.otx_api import OTXAPI


class BottleDetector(OTXAPI):
    """OTX API를 상속받아 object detection을 수행하는 클래스"""

    PET_BOTTLE_MODEL = {
        "model_template_path": "resources/pet_bottle_detection/template",
        "model_weight_path": "resources/pet_bottle_detection/model/model.xml",
        "model_name": "Custom_Object_Detection_YOLOX"
        }
    GLASS_BOTTLE_MODEL = {
        "model_template_path": "resources/glass_bottle_detection/template",
        "model_weight_path": "resources/glass_bottle_detection/model/model.xml",
        "model_name": "Custom_Object_Detection_YOLOX"
        }

    def __init__(self):
        super().__init__()
        self.current_target = None
        self.set_model_target()

    def __str__(self):
        """현재 model이 target하고 있는 물체의 이름을 리턴합니다."""
        return self.current_target

    def set_model_target(self, target="pet"):
        """model을 통해 detection하고자 하는 물체를 지정합니다."""
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

    def detect_bottle(self, frame) -> tuple:
        """프레임 안에서 target 물체가 있는지 detection을 수행합니다.

        return: (detection되었는지여부, accuracy, cropframe좌표)
        """
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]
        predictions, _ = self._get_predictions(frame)

        detected = False if not predictions else True

        if detected is False:
            prediction_accuracy = None
            crop_frame_coordinate = None
        else:
            prediction = predictions[-1]
            box_x1 = frame_width * prediction.shape.x1
            box_y1 = frame_height * prediction.shape.y1
            box_width = frame_width * prediction.shape.width
            box_height = frame_height * prediction.shape.height

            box_y1 += 100

            prediction_accuracy = prediction.get_labels()[-1].probability * 100
            crop_frame_coordinate = (int(box_x1), int(box_y1),
                                     int(box_x1+box_width),
                                     int(box_y1+box_height))

        return (detected, prediction_accuracy, crop_frame_coordinate)
