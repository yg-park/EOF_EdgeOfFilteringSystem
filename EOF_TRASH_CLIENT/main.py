"""
이 파일은 분류라인 프로그램을 시작하는 파일입니다.
"""
from lane_control import LaneController


def main():
    """엔트리포인트"""
    lane_1 = LaneController()
    lane_1.execute()


if __name__ == "__main__":
    main()
