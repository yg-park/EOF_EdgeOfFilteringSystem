# EOF:EOF - "Edge Of Filtering system"
불완전하게 분리수거 된 재활용품에 대한 최종분류 시스템
============
## 프로젝트 설명
프로젝트 주제: OpenCV 영상처리 라이브러리를 활용한 프로그램 만들기<br>
<br>
프로젝트 수행자: 인텔 엣지AI SW개발자 아카데미 3기 / 팀 EOF (권강현, 박도현, 박용근, 우창민)<br>
<br>
프로젝트 수행기간: 23/12/28 ~ 24/01/16<br>

<br>
<br>



* 최상의 재활용 원료를 확보하기 위해 원료 품질을 떨어뜨리는 케이스의 재활용 쓰레기들을 한번 더 분류해주는 시스템

* 쓰레기 분류라인에 있는 작업자가 음성인식을 통해 자유자재로 분류모델을 변경하며, 재활용 쓰레기 분류작업을 진행하도록 하는 것이 최종 목표
<br>

## Clone code
```shell
git clone https://github.com/yg-park/EOF_SeparateTrashCollection.git
```
<br>

## Contents:
 - <font size="+1">[프로젝트 개발 동기](#motivation)</font>
 - <font size="+1">[개발환경 구축](#prerequisite)</font>
 - <font size="+1">[모델 소개](#used-ai-model)</font>
 - <font size="+1">[SW Design](#sw-design)</font>
 - <font size="+1">[Output](#output)</font>
<br><br>

## Motivation
<br><br>

유스케이스 시나리오는 아래와 같다.

```
첫번째 재활용 포대A에는 라벨이 남아있는 투명페트병과 라벨이 제거된 투명페트병이 담겨있다.
두번째 재활용 포대B에는 철뚜껑이 남아있는 유리병과 철뚜껑이 제거된 유리병이 담겨있다.


근무자가 포대A(투명 페트병)를 분류 라인에 쏟았다. 
페트병을 분류하는 모델이 적용된 컨베이어벨트 라인이 돌아간다.
현재 컨베이어 벨트 라인은 페트병을 분류하는 모델이 적용 되어있다.
라벨이 남아있는 투명페트병은 컨베이어벨트 진행 도중에 분류되어 쳐내져서 포대C에 담기고, 라벨이 제거되어있는 투명페트병은 컨베이어벨트 끝까지 진행되어 포대D에 담긴다.
첫번째 재활용 포대A(투명 페트병)에 대한 분류가 끝이 났다.


근무자가 포대B(유리병)를 분류 라인에 쏟았다. 
근무자는 마이크 음성인식을 통해 컨베이어벨트에 적용된 분류모델을 변경한다.
현재 컨베이어 벨트 라인은 유리병을 분류하는 모델이 적용 되어있다.
철뚜껑이 남아있는 유리병은 컨베이어벨트 진행 도중에 쳐내져서 포대E에 담기고, 철뚜껑이 제거되어있는 유리병은 컨베이어벨트 끝까지 진행되어 포대F에 담긴다.
두번째 재활용 포대B(유리병)에 대한 분류가 끝이 났다.
```
<br>

## Prerequisite
 - <font size="+1">[환경 구축 방법 - 서버](EOF_TRASH_SERVER/README.md#top)</font>
 - <font size="+1">[환경 구축 방법 - 클라이언트](EOF_TRASH_CLIENT/README.md#top)</font>
<br>


## SW Design
 - <font size="+1">[High Level Design](#high-level-design)</font>
 - <font size="+1">[Gantt Chart](#gantt-chart)</font>
 - <font size="+1">[Flow Chart](#flowchart)</font>
 - <font size="+1">[Class Diagram](#class-diagram)</font>
<br>

### High Level Design
![High Level Design](./Documents/Design/SW/high_level_design.png)
<br>

### Gantt Chart
![Gantt Chart](./Documents/Design/Gantt_Chart.png)
<br>

### Flow Chart
![Flow Chart](./Documents/Design/Flow_Chart.png)
<br>

### Class Diagram
![Class Diagram](./Documents/Design/Class_Diagram.png)
<br>

## Used AI Model
** 아래 텍스트를 누르면 상세 설명 링크로 연결됩니다.
 - [페트병 - 분류](EOF_TRASH_SERVER/resources/pet_bottle_classification/README.md#top)
 - [페트병 - 감지](EOF_TRASH_SERVER/resources/pet_bottle_detection/README.md#top)
 - [유리병 - 분류](EOF_TRASH_SERVER/resources/glass_bottle_classification/README.md#top)
 - [유리병 - 감지](EOF_TRASH_SERVER/resources/glass_bottle_detection/README.md#top)
 - [whisper - 음성 인식](EOF_TRASH_SERVER/resources/whisper/README.md#top)
 - [llama2 - 텍스트 생성](EOF_TRASH_SERVER/resources/llama2/README.md#top)

<br>

## Output
<br>

### GUI
![SERVER_Main_GUI_Frame](/Documents/Design/UI/GUI_MainFrame.png)
<br>




<br>


## 프로젝트 시연 영상
(아래 이미지를 클릭하시면 유튜브로 이동합니다.)<br>
[![프로젝트 시연영상](/Documents/Design/README_THUMB/http://img.youtube.com/vi/hgrCi_iDWEE/2.jpg)](https://youtu.be/hgrCi_iDWEE)<br>
<br>
<br>


## 프로젝트 발표 자료
(아래 이미지를 클릭하시면 구글 슬라이드로 이동합니다.)<br>
[![프로젝트 발표자료](/Documents/Design/README_THUMB/project_ppt_thumbnail.jpg)](https://docs.google.com/presentation/d/11SBK1dMmhwi1lo105HpmOrtBrURcBn-eqiIlg8w-Vn8/edit?usp=sharing)<br>
<br>
<br>


## 프로젝트 개발 명세서
(아래 이미지를 클릭하시면 구글 드라이브로 이동합니다.)
[![프로젝트 개발명세서](/Documents/Design/README_THUMB/project_doc_thumbnail.jpg)](https://drive.google.com/file/d/1-3zh4HGUDPPjZDXAhenZUYnj1TJ6g7hT/view?usp=sharing)<br>
<br>
<br>

<!-- 



-->