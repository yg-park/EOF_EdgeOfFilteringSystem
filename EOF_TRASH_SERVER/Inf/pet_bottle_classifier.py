"""
영상 프레임 속 페트병의 비닐라벨 부착여부를 판별하는 모델입니다.
"""
import time
import cv2
from otx.api.configuration.helper import create as create_parameters_from_parameters_schema
from otx.api.entities.task_environment import TaskEnvironment
from otx.cli.registry import Registry
from otx.cli.utils.io import read_label_schema, read_model
from otx.cli.utils.importing import get_impl_class
from otx.api.entities.inference_parameters import InferenceParameters
from otx.api.entities.annotation import AnnotationSceneEntity, AnnotationSceneKind
from otx.api.entities.dataset_item import DatasetItemEntity
from otx.api.entities.datasets import DatasetEntity
from otx.api.entities.image import Image


class PetBottleClassifier:
    """OTX API를 통해 만들어진 AI모델을 로드하는 클래스"""

    model_template_path = "resources/pet_bottle_classification/template"
    model_weight_path = "resources/pet_bottle_classification/model/model.xml"
    model_name = "Custom_Image_Classification_MobileNet-V3-large-1x"

    def __init__(self):
        self.task = self._init_task()

    def _init_task(self):
        registry = Registry(self.model_template_path)
        template = registry.get(self.model_name)
        hyper_parameters = template.hyper_parameters.data
        hyper_parameters = create_parameters_from_parameters_schema(hyper_parameters)
        environment = TaskEnvironment(
            model=None,
            hyper_parameters=hyper_parameters,
            label_schema=read_label_schema(self.model_weight_path),
            model_template=template,
            )
        environment.model = read_model(
            environment.get_model_configuration(), self.model_weight_path, None
            )
        task_class = (get_impl_class(template.entrypoints.openvino)
                      if self.model_weight_path.endswith(".xml")
                      else get_impl_class(template.entrypoints.base))
        task = task_class(task_environment=environment)
        return task

    def _get_predictions(self, frame):
        """Returns list of predictions made by task on a frame."""

        empty_annotation = AnnotationSceneEntity(annotations=[], kind=AnnotationSceneKind.PREDICTION)

        item = DatasetItemEntity(
            media=Image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)),
            annotation_scene=empty_annotation,
        )

        dataset = DatasetEntity(items=[item])

        start_time = time.perf_counter()
        predicted_validation_dataset = self.task.infer(
            dataset,
            InferenceParameters(is_evaluation=True),
        )
        elapsed_time = time.perf_counter() - start_time
        item = predicted_validation_dataset[0]
        return item.get_annotations(), elapsed_time

    def classify_pet_bottle(self, frame):
        """비닐 라벨이 제거된 페트병이면 0을 리턴하고,
        비닐라벨이 제거되지 않은 페트병이면 1을 리턴한다."""

        prediction, _ = self._get_predictions(frame)
        return int(prediction[-1].get_labels()[-1].get_label().id)        
