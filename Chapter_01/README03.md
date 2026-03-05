## 3️⃣ 마우스 영역 선택 및 ROI 추출 (E01_3)

설명

사용자가 마우스로 이미지에서 사각형 영역을 드래그하면 그 영역을 ROI로 추출하여 별도 창에 표시하고, 필요시 파일로 저장할 수 있다.

### 코드 (E01_3.py)

```python
# 파일 경로 처리를 위해 os 모듈 불러오기
import os

# OpenCV 라이브러리를 cv라는 이름으로 불러오기
import cv2 as cv

# 배열 및 이미지 처리를 위해 numpy 라이브러리 불러오기
import numpy as np

# 파일 저장 시 시간 정보를 사용하기 위해 time 모듈 불러오기
import time


# 사용할 이미지 파일 이름 설정
path = "soccer.jpg"

# 현재 실행 중인 파이썬 파일의 절대 경로를 가져오기
script_dir = os.path.dirname(os.path.abspath(__file__))

# 현재 스크립트 파일이 있는 폴더와 soccer.jpg 파일을 결합하여 전체 경로 생성
path = os.path.join(script_dir, "soccer.jpg")


# OpenCV를 이용하여 이미지를 컬러(BGR) 형식으로 불러오기
img = cv.imread(path, cv.IMREAD_COLOR)

# 이미지가 정상적으로 로드되지 않았을 경우 예외 발생
if img is None:
	raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {os.path.abspath(path)}")

# 원본 이미지를 복사하여 별도로 저장 (ROI 선택 시 원본 유지 목적)
orig = img.copy()
# 현재 마우스로 드래그 중인지 여부를 저장하는 변수
drawing = False
# 마우스 클릭 시작 좌표를 저장할 변수 초기화
ix = iy = -1
# ROI 영역의 좌표를 저장할 변수 초기화
rx1 = ry1 = rx2 = ry2 = 0
# ROI가 선택되었는지 여부를 나타내는 변수
selected = False
# 추출된 ROI 이미지를 저장할 변수
roi = None

# 마우스 이벤트를 처리하는 함수 정의
def mouse_callback(event, x, y, flags, param):

	# 함수 내부에서 전역 변수 사용 선언
	global ix, iy, drawing, rx1, ry1, rx2, ry2, selected, roi

	# 마우스 왼쪽 버튼을 눌렀을 때
	if event == cv.EVENT_LBUTTONDOWN:

		# 드래그 시작 상태로 변경
		drawing = True

		# 이전 선택 상태 초기화
		selected = False

		# 시작 좌표 저장
		ix, iy = x, y

	# 마우스를 이동했을 때
	elif event == cv.EVENT_MOUSEMOVE:

		# 드래그 중이라면
		if drawing:

			# 시작 좌표와 현재 좌표를 이용하여 사각형 영역 계산
			rx1, ry1 = min(ix, x), min(iy, y)
			rx2, ry2 = max(ix, x), max(iy, y)

	# 마우스 왼쪽 버튼을 놓았을 때
	elif event == cv.EVENT_LBUTTONUP:

		# 드래그 상태 종료
		drawing = False

		# 최종 ROI 좌표 계산
		rx1, ry1 = min(ix, x), min(iy, y)
		rx2, ry2 = max(ix, x), max(iy, y)

		# 선택한 영역의 크기가 유효한지 확인
		if rx2 - rx1 > 0 and ry2 - ry1 > 0:

			# numpy 슬라이싱을 이용하여 ROI 영역 추출
			roi = orig[ry1:ry2, rx1:rx2].copy()

			# ROI가 선택되었음을 표시
			selected = True

			# ROI 이미지를 별도의 창에 출력
			cv.imshow("ROI", roi)


# 프로그램 창 제목 설정
window = "ROI Selector - drag to select, r: reset, s: save, q: quit"

# OpenCV 윈도우 생성
cv.namedWindow(window, cv.WINDOW_AUTOSIZE)

# 해당 창에서 발생하는 마우스 이벤트를 mouse_callback 함수로 연결
cv.setMouseCallback(window, mouse_callback)


# 프로그램이 계속 실행되도록 무한 루프 생성
while True:

	# 원본 이미지를 복사하여 화면 출력용 이미지 생성
	disp = orig.copy()

	# 현재 드래그 중이라면
	if drawing:

		# 드래그 중인 사각형 영역을 화면에 표시
		cv.rectangle(disp, (rx1, ry1), (rx2, ry2), (0, 255, 0), 2)

	# 이미 ROI가 선택된 상태라면
	elif selected:

		# 선택된 ROI 영역을 화면에 사각형으로 표시
		cv.rectangle(disp, (rx1, ry1), (rx2, ry2), (0, 255, 0), 2)

	# 현재 화면 이미지를 윈도우에 출력
	cv.imshow(window, disp)

	# 키보드 입력을 1ms 동안 대기 후 입력값 저장
	key = cv.waitKey(1) & 0xFF

	# 'q' 키 또는 ESC 키를 누르면 프로그램 종료
	if key == ord('q') or key == 27:
		break

	# 'r' 키를 누르면 ROI 선택 상태 초기화
	elif key == ord('r'):

		# ROI 선택 상태 해제
		selected = False

		# ROI 데이터 초기화
		roi = None

		# ROI 창이 열려 있다면 닫기
		cv.destroyWindow("ROI")

	# 's' 키를 누르면 ROI 저장
	elif key == ord('s'):

		# ROI가 선택되어 있는 경우에만 저장
		if selected and roi is not None:

			# ROI 좌표와 현재 시간을 이용하여 파일 이름 생성
			fname = f"roi_{rx1}_{ry1}_{rx2}_{ry2}_{int(time.time())}.png"

			# ROI 이미지를 파일로 저장
			cv.imwrite(fname, roi)
			# 저장된 파일의 절대 경로를 출력
			print(f"Saved ROI to {os.path.abspath(fname)}")

# 모든 OpenCV 창을 닫기
cv.destroyAllWindows()
```


주요 사용 함수 및 처리 흐름

- `cv.setMouseCallback(window, callback)` — 드래그 시작점/이동/종료 이벤트 처리
- 드래그 중에는 `cv.rectangle()`로 현재 선택 영역을 시각화
- ROI 추출: NumPy 슬라이싱 `roi = img[y1:y2, x1:x2].copy()`
- `cv.imshow("ROI", roi)`로 별도 창에 표시
- 키 처리: `r` → 리셋, `s` → 파일 저장, `q` → 종료

# 실행

```powershell
cd Chapter_01
env\Scripts\python.exe E01_3.py
```
# 결과

![E01_3 preview](E01/E01_3.png)

---





