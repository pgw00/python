import os
import cv2 as cv
import sys
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, "soccer.jpg")

# 컬러 이미지 로드
img = cv.imread(path, cv.IMREAD_COLOR)
if img is None:
    raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {os.path.abspath(path)}")

print("original shape:", img.shape, "dtype:", img.dtype)

# 그레이스케일 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 화면 표시용 (흑백을 3채널로 변환)
gray_display = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

# 원본 + 흑백 연결
combined = np.hstack((img, gray_display))

scale = 0.5
resized = cv.resize(combined, None, fx=scale, fy=scale)

# 화면 출력
cv.imshow("Original (left) | Gray (right)", resized)
cv.waitKey(0)
cv.destroyAllWindows()

# 파일 저장
cv.imwrite("gray_output.jpg", gray)
cv.imwrite("combined_output.jpg", combined)

print("Saved: gray_output.jpg, combined_output.jpg")