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
pip install opencv-python-headless==4.8.1.78
```
라이브러리 사용을 위해 가상환경에 패키지를 설치한다.
openvino와 opencv의  버전충돌로 인해 PyQt5 GUI가 제대로 출력이 안되는 경우를 막기 위해 opencv-python-headless는 별도로 설치한다.


### Configure an IP address
```shell
EOF_TRASH_SERVER/resources/communication_config.ini
파일 내부 SERVER 및 LANE_1 IP 환경에 맞게 수정
```
자신의 환경에 맞게 IP를 수정한다.
<br><br>

### prepare API key for LLAMA2
```shell
EOF_TRASH_SERVER/resources/api_tokens.ini
파일 내부 MODEL 및 REPLICATE 에 알맞은 모델과 API key 를 적는다.
```
사용할 모델의 API key 와 replicate 를 사용하기 위해 부여받은 개인 API key 를 적는다.
<br><br>

## Steps to run

```shell
cd EOF_SeparateTrashCollection/EOF_TRASH_SERVER/
source .server_venv/bin/activate
python3 main.py
#GUI 최하단에서 /activate LANE_1 명령어 입력으로 1번 레인 작동
#GUI 최하단에서 /deactivate LANE_1 명령어 입력으로 레인 정지
#GUI 최하단에서 /change model 명령어 입력으로 레인에 사용되는 모델 변경
```

만약 위 절차를 따라서 설치를 했음에도 실행이 되지 않는다면 아래의 오류 메시지인지 확인하라.

1. xcb 플러그인 자체가 없는 경우
```plain
python3 main.py 
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.

Aborted (core dumped)
```
위 문제가 발생할때는 아래 패키지를 설치해보라
```shell
sudo apt-get install libxcb-xinerama0
```
<br>

2. PyQt Plugin 초기화 실패 문제 (xcb, wayland)

여러 환경에서 진행해보았으나, 어떤 곳은 xcb 환경에서 작동 가능하고, 어떤 곳은 wayland 환경에서 작동한다.
이에 대한 어떠한 연관성도 찾지 못하였다. 여러분의 컴퓨터에 맞는 plugin을 찾아 사용하면 되겠다.

```plain
Warning: Ignoring XDG_SESSION_TYPE=wayland on Gnome. Use QT_QPA_PLATFORM=wayland to run on Wayland anyway.
qt.qpa.plugin: Could not find the Qt platform plugin "wayland" in ""
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: xcb.

Aborted (core dumped)
```
위 문제가 발생할때는 아래 플러그인을 적용해보라
```shell
export QT_QPA_PLATFORM=wayland
```
만약 에러메시지가 wayland가 아닌 xcb로 나온다면 아래 명령어를 치면 된다.
```shell
export QT_QPA_PLATFORM=xcb
```
<br><br>

## Output

* (서버 GUI 화면)

![GUI_MainFrame](/Documents/Design/UI/GUI_MainFrame.png)

<br>
* (서버 프로그램 실행용 아이콘)

![ProgramLaunchICon](/Documents/Design/UI/ProgramLaunchICon.png)
<br><br>

## Appendix
참고 자료 및 알아두어야할 사항들

* PyQt5 GUI Programming
* Qthread Multi-Threading
* Python Threading GIL(Global Interpreter Lock)
* Queue
* TCP / IP 통신
* AI 모델을 활용한 추론
