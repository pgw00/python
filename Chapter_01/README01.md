# OpenCV 실습 1주차 과제

![Capture](soccer.jpg)

컴퓨터비전 수업에서 OpenCV 라이브러리를 활용하여 이미지 처리와 마우스 이벤트를 이용한 인터랙티브 프로그램을 구현하였다.
각 실습은 이미지 처리의 기본 개념과 사용자 입력을 활용한 기능 구현을 목표로 한다.

### 캡처(이미지 취득) 및 기초 개념 정리

![Capture](E01/capture.png)


- 이미지(픽셀): 이미지는 가로×세로 격자에 각 위치마다 색상값(채널)을 가진 배열로 표현된다. 예: 컬러 이미지는 3채널(B, G, R).
- 해상도(Resolution): 이미지의 크기(가로×세로 픽셀 수)는 취득 장치나 저장된 파일에 따라 달라진다.
- 샘플링과 양자화: 센서는 연속 광학 신호를 격자(샘플)로 샘플링하고, 각 샘플은 정수값(양자화)으로 저장된다.
- 색공간과 채널 순서: OpenCV는 이미지를 BGR 순서로 로드하므로 색 관련 처리를 할 때 RGB와의 순서 차이를 주의해야 한다.
- 그레이스케일 변환(예): 일반적으로 인간 시각의 감도에 따라 가중합을 사용한다.
	- Y = 0.299·R + 0.587·G + 0.114·B (OpenCV의 `cv.COLOR_BGR2GRAY`는 내부적으로 유사한 변환을 수행)

위 개념은 E01_1의 이미지 로드와 색상 변환, E01_3의 ROI 추출 등 모든 실습의 기반이 된다.

---

## 1️⃣ 이미지 불러오기 및 그레이스케일 변환 (E01_1)


---

### 코드 (E01_1.py)

```python
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
```

설명

이미지를 로드한 뒤 원본 컬러 영상과 그레이스케일 영상을 나란히 보여준다. 이미지 로드, 색상 변환, 배열 결합, 화면 표시의 기본 흐름을 학습한다.

주요 사용 함수 및 처리 흐름

- `cv.imread(path, cv.IMREAD_COLOR)` — 이미지 파일 로드
- `cv.cvtColor(img, cv.COLOR_BGR2GRAY)` — BGR → 그레이스케일 변환
- `cv.cvtColor(gray, cv.COLOR_GRAY2BGR)` — 그레이 이미지를 3채널로 복원(나란히 붙일 때 색상 채널 맞춤)
- `np.hstack((img, gray_display))` — 원본과 그레이 이미지를 가로로 결합
- `cv.resize(..., fx, fy)` — 표시용으로 축소(선택사항)
- `cv.imshow()` / `cv.waitKey()` — 화면 출력 및 키 입력 대기

실행

```powershell
cd Chapter_01
env\Scripts\python.exe E01_1.py
```
결과

![E01_1 preview](E01/E01_1.jpg)
