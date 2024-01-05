"""
영상 프레임에서 유리병을 찾는 모듈입니다.
"""
from Inference.otx_api import OTXAPI


class GlassBottleDetector(OTXAPI):
    """OTX API를 통해 유리병 object detection을 수행하는 클래스"""
    model_template_path = "resources/glass_bottle_detection/template"
    model_weight_path = "resources/glass_bottle_detection/model/model.xml"
    model_name = "Custom_Object_Detection_Gen3_ATSS"

    def detect_pet_bottle(self, frame) -> tuple:
        """ 영상 frame에서 페트병 object들을 detect하고,
            frame의 중앙선을 지나는 페트병 object box가 있으면, "True"와 "페트병 영역이 crop된 이미지"를 리턴한다.
            그 외의 모든 경우에는 "False"와 "None"을 리턴한다.

            사용 예)
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()

            petDetector = PetBottleDetector()
            ret, frame = petDetector.detect_pet_bottle(frame)
        """
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]
        predictions, _ = self._get_predictions(frame)

        if not predictions:  # not(리스트가 비어 있으면 True 반환)
            return False, False, (0, 0, frame_width, frame_height)

        # 뭔가 detection이 되긴 했는데 정확도가 제대로 높은게 들어온건지 확인해야 함
        cnt = 0
        for prediction in predictions:
            # 오브젝트 박스의 probability 백분율 / 단일 레이블 모델이기 때문에 [-1]로 인덱스 접근함
            box_probability = prediction.get_labels()[-1].probability * 100
            if box_probability < 80.0:
                continue
            else:
                cnt += 1

        # 뭔가 detection은 되었지만 정확도 허들을 넘는게 하나도 없어서 원본 프레임 그대로 리턴하는 상태
        if cnt == 0:
            return False, False, (0, 0, frame_width, frame_height)


        # 정확도를 충족하는 것들이 있는 경우 
        for prediction in predictions:
            box_x1 = frame_width * prediction.shape.x1
            box_y1 = frame_height * prediction.shape.y1
            box_width = frame_width * prediction.shape.width
            box_height = frame_height * prediction.shape.height

            box_x_center = box_x1 + box_width/2  # 오브젝트 박스의 중앙 x좌표
            if int(box_x_center) == int(frame_width/2):
                return True, True, (int(box_x1), int(box_y1),
                                    int(box_x1+box_width),
                                    int(box_y1+box_height))

        return True, False, (int(box_x1), int(box_y1),
                             int(box_x1+box_width),
                             int(box_y1+box_height))
