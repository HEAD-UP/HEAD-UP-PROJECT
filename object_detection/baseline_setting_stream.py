import cv2

# 1. Initial Setting and Declare Function
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

# 2. Click the point in streaming video
cap = cv2.VideoCapture(0)
ret = True

while (ret):
    ret, image_np = cap.read()
    cv2.imshow('stream version', image_np)

    # Mouse Click Function
    cv2.setMouseCallback('stream version', get_mouse_click_location)
    if mouse_count == 0:
        break
    if cv2.waitKey(25) & 0xFF == ord('q'):  # waitKey( 내부의 값이 작아지면 CPU 의 부담은 커지는데 비해 처리속도는 빨라짐 )
        break

cv2.destroyAllWindows()
cap.release()

# 3. Save the value {a, b, c} into file
f = open("output_stream.txt",'w')
data = str(a) + " " + str(b) + " " + str(c)
f.write(data)
f.close()