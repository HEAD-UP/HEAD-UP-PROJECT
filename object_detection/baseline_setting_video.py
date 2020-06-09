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

# 2. Click the point in stored video
inputVideo = '.\\video_samples\\s1_b.mp4'

# Raspbian Version
# inputVideo = './video_samples/s1_b.mp4'

cap = cv2.VideoCapture(inputVideo)
ret = True

while (ret):
    ret, image_np = cap.read()
    cv2.imshow('stored version', image_np)

    # Mouse Click Function
    cv2.setMouseCallback('stored version', get_mouse_click_location)
    if mouse_count == 0:
        break

    # waitKey(value down -> more CPU)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    # Get time when the video ends
    if (cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT)):
        break

cv2.destroyAllWindows()
cap.release()

# 3. Save the value {a, b, c} into file
f = open("output_video.txt",'w')
data = str(a) + " " + str(b) + " " + str(c)
f.write(data)
f.close()