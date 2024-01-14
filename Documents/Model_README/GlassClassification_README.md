# 유리병 classification 모델
<a name="top"></a>

## 240110
### backbone
Custom_Image_Classification_DeiT-Tiny (otx 제공 pretrained model)
### data
- 2175장의 데이터
  - 자체 수집 데이터 : 1005장(Clear 490장 | Lid 515장)
  - AI hub 데이터 : 1170장(Clear 590장 | Lid 580장)
- 수집 방법 : 자체 수집 데이터 - 직접 촬영한 사진을 data augmentation 해서 증강<br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;AI hub 데이터 - 자체 데이터와 비슷한 사진을 직접 선별
- 8:2의 비율로 training:validation 셋팅
### Model 전이학습 과정
1. otx build
2. train
3. export
4. deploy
### Model별 Training 결과
1차 : EfficientNet-V2-S(97%)&ensp;|&ensp;DeiT-Tiny(97%)&ensp;|&ensp;MobileNet-V3-large-1x(96%)&ensp;|&ensp;EfficientNet-B0(95.5%)<br>
2차 : EfficientNet-V2-S(97.7%)&ensp;|&ensp;DeiT-Tiny(97.5%)&ensp;|&ensp;MobileNet-V3-large-1x(96.5%)&ensp;|&ensp;EfficientNet-B0(96.5%)<br>
3차 : DeiT-Tiny(100%)&ensp;|&ensp;EfficientNet-V2-S(99.7%)&ensp;|&ensp;MobileNet-V3-large-1x(98.2%)&ensp;|&ensp;EfficientNet-B0(98%)
### Best Accuracy
100%

- [다른 AI 모델 보기](/README.md#used-ai-model)

<!-- ## 240104
### backbone
Custom_Image_Classification_EfficientNet-V2-S (otx 제공 pretrained model)
### data
- 1000장의 데이터
  - 500장: 자체 수집 데이터
  - 500장: AI hub 데이터
- 8:2의 비율로 training:validation 셋팅
### accuracy
97.0% -->

