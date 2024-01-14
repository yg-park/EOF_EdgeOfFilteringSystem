# 페트병 classification 모델
<a name="top"></a>

## 240104
### backbone
Custom_Image_Classification_EfficientNet-V2-S (otx 제공 pretrained model)
### data
- 1062장의 데이터
  - 자체 수집 데이터 : 592장(Clear 283장 | Label 299장)
  - 470장: AI hub 데이터
- 수집 방법 : 자체 수집 데이터 - 직접 촬영한 사진을 data augmentation 해서 증강<br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;AI hub 데이터 - 자체 데이터와 비슷한 사진을 직접 선별
- 8:2의 비율로 training:validation 셋팅
### Model 전이학습 과정
1. otx build
2. train
3. export
4. deploy
### Model별 Training 결과
1차 : EfficientNet-V2-S(99.5%)&ensp;|&ensp;DeiT-Tiny(99.3%)&ensp;|&ensp;EfficientNet-B0(98.7%)&ensp;|&ensp;MobileNet-V3-large-1x(97.6%)
### Best Accuracy
99.5%

- [다른 AI 모델 보기](/README.md#used-ai-model)
