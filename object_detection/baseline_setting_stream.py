import cv2
# 1. 초기 세팅 및 함수 정의
def set_baseline(x1, y1, x2, y2):
    return y2 - y1, x1 - x2, x2 * y1 - x1 * y2

baseline_x = []
baseline_y = []
mouse_count = 2

def get_mouse_click_location(event, x, y, flags, param):
    global mouse_count, a, b, c
    if (mouse_count > 0 and event == cv2.EVENT_LBUTTONDOWN):
        baseline_x.append(x)
        baseline_y.append(y)
        mouse_count = mouse_count - 1
        if (mouse_count == 0):
            a, b, c = set_baseline(baseline_x[0] * 0.001, baseline_y[0] * 0.001, baseline_x[1] * 0.001, baseline_y[1] * 0.001)

# 2. 스트리밍 영상에서 마우스를 사용해서 좌표 클릭
cap = cv2.VideoCapture(0)
ret = True

while (ret):
    ret, image_np = cap.read()
    cv2.imshow('stream version', image_np)

    # Mouse Click 좌표를 위한 함수
    cv2.setMouseCallback('stream version', get_mouse_click_location)
    if mouse_count == 0:
        break
    if cv2.waitKey(25) & 0xFF == ord('q'):  # waitKey( 내부의 값이 작아지면 CPU 의 부담은 커지는데 비해 처리속도는 빨라짐 )
        break

cv2.destroyAllWindows()
cap.release()

# 3. 파일에 저장 (a, b, c)
f = open("output_stream.txt",'w')
data = str(a) + " " + str(b) + " " + str(c)
f.write(data)
f.close()