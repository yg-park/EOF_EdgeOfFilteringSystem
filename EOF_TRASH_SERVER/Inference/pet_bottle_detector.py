"""
영상 프레임에서 페트병을 찾는 모듈입니다.
"""
from Inference.otx_api import OTXAPI


class PetBottleDetector(OTXAPI):
    """OTX API를 통해 페트병 object detection을 수행하는 클래스"""
    model_template_path = "resources/pet_bottle_detection/template"
    model_weight_path = "resources/pet_bottle_detection/model/model.xml"
    model_name = "Custom_Object_Detection_YOLOX"

    def detect_pet_bottle(self, frame) -> tuple:
        """프레임 안에서 페트병이 있는지 detection을 수행합니다.

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

            prediction_accuracy = prediction.get_labels()[-1].probability * 100
            crop_frame_coordinate = (int(box_x1), int(box_y1),
                                     int(box_x1+box_width),
                                     int(box_y1+box_height))

        return (detected, prediction_accuracy, crop_frame_coordinate)
