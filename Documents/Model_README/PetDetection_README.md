# 페트병 detection 모델
<a name="top"></a>

## 240104
### backbone
Custom_Object_Detection_YOLOX (otx 제공 pretrained model)
### data
- 1062장의 데이터
  - 자체 수집 데이터 : 592장(Clear 283장 | Label 299장)
  - 470장: AI hub 데이터
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
1차 : YOLOX(100%)&ensp;|&ensp;Gen3_ATSS(99.2%)&ensp;|&ensp;Gen3_SSD(98.4%)
### Best Accuracy
100%

- [다른 AI 모델 보기](/README.md#used-ai-model)
