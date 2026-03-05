import cv2 as cv
import sys
import os
path = "soccer.jpg"
script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, "soccer.jpg")

# 이미지 로드
img = cv.imread(path, cv.IMREAD_COLOR)

if img is None:
    print("이미지를 찾을 수 없습니다.")
    sys.exit()

brush_size = 5  # 초기 붓 크기
drawing = False


def paint(event, x, y, flags, param):
    global drawing, brush_size

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        cv.circle(img, (x, y), brush_size, (255, 0, 0), -1)  # 파란색

    elif event == cv.EVENT_RBUTTONDOWN:
        drawing = True
        cv.circle(img, (x, y), brush_size, (0, 0, 255), -1)  # 빨간색

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            if flags & cv.EVENT_FLAG_LBUTTON:
                cv.circle(img, (x, y), brush_size, (255, 0, 0), -1)
            elif flags & cv.EVENT_FLAG_RBUTTON:
                cv.circle(img, (x, y), brush_size, (0, 0, 255), -1)

    elif event == cv.EVENT_LBUTTONUP or event == cv.EVENT_RBUTTONUP:
        drawing = False


cv.namedWindow("Paint")
cv.setMouseCallback("Paint", paint)

while True:
    cv.imshow("Paint", img)

    key = cv.waitKey(1) & 0xFF

    if key == ord('+'):
        brush_size = min(15, brush_size + 1)
        print("Brush size:", brush_size)

    elif key == ord('-'):
        brush_size = max(1, brush_size - 1)
        print("Brush size:", brush_size)

    elif key == ord('q'):
        break

cv.destroyAllWindows()