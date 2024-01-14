# 유리병 detection 모델
<a name="top"></a>

## 240114
### backbone
Custom_Object_Detection_YOLOX (otx 제공 pretrained model)
### data
- 2175장의 데이터
  - 자체 수집 데이터 : 1005장(Clear 490장 | Lid 515장)
  - AI hub 데이터 : 1170장(Clear 590장 | Lid 580장)
- 수집 방법 : 자체 수집 데이터 - 직접 촬영한 사진을 data augmentation 해서 증강<br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;AI hub 데이터 - 자체 데이터와 비슷한 사진을 직접 선별
- 7:2:1의 비율로 training:validation:test 셋팅
### Model 전이학습 과정
1. datumaro로 데이터셋을 구축
2. otx build
3. train
4. export
5. deploy
### Model별 Training 결과
1차 : Gen3_ATSS(92%)&ensp;|&ensp;YOLOX(89%)&ensp;|&ensp;Gen3_SSD(87.6%)<br>
2차 : Gen3_ATSS(99.9%)&ensp;|&ensp;YOLOX(97.4%)&ensp;|&ensp;Gen3_SSD(96%)<br>
3차 : 기존의 Gen3_ATSS 모델을 사용중에 프레임이 밀리는 현상이 있어 YOLOX 모델로 변경
### Best Accuracy
99.9%

- [다른 AI 모델 보기](/README.md#used-ai-model)

<!-- ## 240104
### backbone
Custom_Object_Detection_Gen3_ATSS (otx 제공 pretrained model)
### data
- 1000장의 데이터
  - 500장: 자체 수집 데이터
  - 500장: AI hub 데이터
- 7:2:1의 비율로 training:validation:test 셋팅
### accuracy
92% -->
