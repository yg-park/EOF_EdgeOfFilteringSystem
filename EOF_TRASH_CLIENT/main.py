"""
이 파일은 분류라인 프로그램을 시작하는 파일입니다.
"""
from EOF_TRASH_CLIENT.line_control import LineController


def main():
    """엔트리포인트"""
    line_1 = LineController()
    line_1.execute()


if __name__ == "__main__":
    main()
