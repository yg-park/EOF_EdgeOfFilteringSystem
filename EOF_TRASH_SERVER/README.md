# SeparateTrashCollection SERVER
<a name="top"></a>

## Prerequisite

* python --verison 3.10.12

<br>

### Activate virtual environment and install packages
```shell
python -m venv .server_venv
source .server_venv/bin/activate
./setup.sh
pip install -U pip
pip install -r requirements.txt
```
라이브러리 사용을 위해 가상환경에 패키지를 설치한다.
<br>

### Configure an IP address
```shell
EOF_TRASH_SERVER/resources/communication_config.ini
파일 내부 SERVER 및 LANE_1 IP 환경에 맞게 수정
```
자신의 환경에 맞게 IP를 수정한다.
<br><br>

### prepare API key for LLAMA2
```shell
EOF_TRASH_SERVER/resources/communication_config.ini
파일 내부 MODEL 및 REPLICATE 에 알맞은 모델과 API key 를 적는다.
```
사용할 모델의 API key 와 replicate 를 사용하기 위해 부여받은 개인 API key 를 적는다.
<br><br>

## Steps to run

```shell
cd EOF_SeparateTrashCollection/EOF_TRASH_SERVER/
source .server_venv/bin/activate
export QT_QPA_PLATFORM=xcb or export QT_QPA_PLATFORM=wayland
(export QT_QPA_PLATFORM 는 자신의 환경에 맞게 사용할 것)
python3 main.py
#GUI 최하단에서 /activate LANE_1 명령어 입력으로 1번 레인 작동
#GUI 최하단에서 /deactivate LANE_1 명령어 입력으로 레인 정지
#GUI 최하단에서 /change model 명령어 입력으로 레인에 사용되는 모델 변경
```

<br><br>

## Output

* (프로젝트 실행 화면 캡쳐)

![./result.jpg](./result.jpg)

<br><br>

## Appendix

* (참고 자료 및 알아두어야할 사항들 기술)
* PyQt5 GUI Programming
* Qthread Multi-Threading
* Python Threading GIL(Global Interpreter Lock)
* Queue
* TCP / IP 통신
* AI 모델을 활용한 추론
