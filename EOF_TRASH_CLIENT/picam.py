import cv2

# 웹캠 열기 (0은 기본 웹캠을 의미)
cap = cv2.VideoCapture(0)

# 웹캠이 정상적으로 열렸는지 확인
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# 무한 루프로 프레임 읽기
while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 프레임 읽기에 문제가 있으면 루프 종료
    if not ret:
        print("Error: Could not read frame.")
        break

    # 프레임을 화면에 표시
    cv2.imshow("Webcam", frame)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 사용한 자원 해제
cap.release()
cv2.destroyAllWindows()
