import os
import cv2 as cv
import numpy as np
import time

path = "soccer.jpg"
script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, "soccer.jpg")


# 이미지 로드
img = cv.imread(path, cv.IMREAD_COLOR)
if img is None:
    raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {os.path.abspath(path)}")

orig = img.copy()
drawing = False
ix = iy = -1
rx1 = ry1 = rx2 = ry2 = 0
selected = False
roi = None

def mouse_callback(event, x, y, flags, param):
    global ix, iy, drawing, rx1, ry1, rx2, ry2, selected, roi
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        selected = False
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            rx1, ry1 = min(ix, x), min(iy, y)
            rx2, ry2 = max(ix, x), max(iy, y)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        rx1, ry1 = min(ix, x), min(iy, y)
        rx2, ry2 = max(ix, x), max(iy, y)
        # 유효한 영역인지 확인
        if rx2 - rx1 > 0 and ry2 - ry1 > 0:
            roi = orig[ry1:ry2, rx1:rx2].copy()
            selected = True
            cv.imshow("ROI", roi)

window = "ROI Selector - drag to select, r: reset, s: save, q: quit"
cv.namedWindow(window, cv.WINDOW_AUTOSIZE)
cv.setMouseCallback(window, mouse_callback)

while True:
    disp = orig.copy()
    if drawing:
        # 드래그 중인 사각형 표시
        cv.rectangle(disp, (rx1, ry1), (rx2, ry2), (0, 255, 0), 2)
    elif selected:
        # 선택된 영역 표시
        cv.rectangle(disp, (rx1, ry1), (rx2, ry2), (0, 255, 0), 2)

    cv.imshow(window, disp)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break
    elif key == ord('r'):
        # 리셋
        selected = False
        roi = None
        # 닫힌 ROI 창이 있으면 제거
        cv.destroyWindow("ROI")
    elif key == ord('s'):
        # 선택된 ROI를 파일로 저장
        if selected and roi is not None:
            fname = f"roi_{rx1}_{ry1}_{rx2}_{ry2}_{int(time.time())}.png"
            cv.imwrite(fname, roi)
            print(f"Saved ROI to {os.path.abspath(fname)}")

cv.destroyAllWindows()
