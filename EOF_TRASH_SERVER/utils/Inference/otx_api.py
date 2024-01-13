"""
OTX API를 통해 추론을 실시하는 모델 클래스들의 부모 클래스가 정의되어 있는 모듈입니다.
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


class OTXAPI:
    """AI 모델 클래스화의 기반이 되는 OTX API를 정의한 부모 클래스"""

    def __init__(self):
        self.task = None

    def _init_task(self, model_template_path, model_weight_path, model_name):
        registry = Registry(model_template_path)
        template = registry.get(model_name)
        hyper_parameters = template.hyper_parameters.data
        hyper_parameters = create_parameters_from_parameters_schema(hyper_parameters)
        environment = TaskEnvironment(
            model=None,
            hyper_parameters=hyper_parameters,
            label_schema=read_label_schema(model_weight_path),
            model_template=template,
            )
        environment.model = read_model(
            environment.get_model_configuration(), model_weight_path, None
            )
        task_class = (get_impl_class(template.entrypoints.openvino)
                      if model_weight_path.endswith(".xml")
                      else get_impl_class(template.entrypoints.base))
        task = task_class(task_environment=environment)
        return task

    def _get_predictions(self, frame):
        empty_annotation = AnnotationSceneEntity(
            annotations=[], kind=AnnotationSceneKind.PREDICTION
        )

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
