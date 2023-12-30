""" 다양한 모델들로 추론하기 위한 프로그램
"""

class Inference:
    def __init__(self):
        """ 다양한 모델들 로드
        """
        
        # TODO: 추론을 하기 위한 다양한 모델들을 로드한다.
        
        # 모델을 로드하는 작업은 일정 시간이 소요가 되기 때문에
        # 미리 로드하지 않고 해당 모델이 필요할 때 로드를 하게 되면
        # 약간의 시간이 소요가 된다.
        # 하지만 미리 로드를 하면 메모리 공간을 차지하게 된다.
    
    def object_detect(self, frame):
        """ 페트병 감지를 위한 추론
        """
        
        # TODO: 페트병 detect
        
        # return ((x2 - x1) / 2 ) + x1 == 320
        # 320 은 카메라 x 좌표의 중심 점
    
    def label_classify(self, roi_in_frame):
        """ 라벨 감지를 위한 추론
        """
        
        # TODO: 라벨 detect 후, 라벨의 유/무 리턴
        
        # return True if the label is being else return false
    
    def voice_interpret(self, void_file_path):
        """ 음성 메세지를 해석하기 위한 추론
        """
        
        # TODO: 음성 메세지를 추론하여 텍스트 