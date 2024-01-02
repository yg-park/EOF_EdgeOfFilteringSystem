"""
이 파일은 분류라인 프로그램을 시작하는 파일입니다.
"""
from lane_control import LaneController


IP_ADDRESS = "10.10.15.58"
UDP_PORT1 = 5555
UDP_PORT2 = 6666
UDP_PORT3 = 7777
UDP_PORT4 = 8888

RC_SERVO_PIN1 = 0
RC_SERVO_PIN2 = 0
SERVO_PIN = 23
ULTRASONIC_TRIGGER_PIN = 2
ULTRASONIC_ECHO_PIN = 3


def main():
    """
    desc: 프로그램 엔트리포인트 함수
    """
    pin = {"RC_SERVO1": RC_SERVO_PIN1, "RC_SERVO2": RC_SERVO_PIN2,
           "ULTRASONIC_TRIG": ULTRASONIC_TRIGGER_PIN,
           "ULTRASONIC_ECHO": ULTRASONIC_ECHO_PIN,
           "SERVO": SERVO_PIN, }
    port = {"PORT_IMAGE": UDP_PORT1, "PORT_STR": UDP_PORT2,
            "PORT_VOICE": UDP_PORT3, "PORT_": UDP_PORT4}

    lane_1 = LaneController(pin, IP_ADDRESS, port)
    lane_1.execute()

    # lane_2 = LaneController(pin, port)
    # lane_2.execute()
    
    # 


if __name__ == "__main__":
    main()
