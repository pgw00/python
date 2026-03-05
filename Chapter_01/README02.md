## 2️⃣ 페인팅 프로그램 (붓 크기 조절 기능, E01_2)

설명

마우스 드래그로 이미지를 그릴 수 있는 간단한 페인팅 도구이다. 좌/우 버튼으로 색을 선택하고 키보드 `+`/`-`로 브러시 크기를 조절한다.


### 코드 (E01_2.py)

```python
# OpenCV 라이브러리를 cv라는 이름으로 불러옴
import cv2 as cv
# 프로그램 종료 등을 위해 sys 모듈 불러오기
import sys
# 파일 경로 처리를 위해 os 모듈 불러오기
import os
# 현재 실행 중인 파이썬 파일의 절대 경로를 가져옴
script_dir = os.path.dirname(os.path.abspath(__file__))
# 현재 스크립트 파일이 있는 폴더 안에 있는 soccer.jpg 파일의 경로 생성
path = os.path.join(script_dir, "soccer.jpg")

# OpenCV를 이용하여 이미지를 컬러(BGR) 형식으로 읽어옴
img = cv.imread(path, cv.IMREAD_COLOR)
# 이미지가 정상적으로 로드되지 않았을 경우 에러 메시지를 출력하고 프로그램 종료
if img is None:
	print("이미지를 찾을 수 없습니다.")
	sys.exit()
# 초기 붓 크기를 5로 설정
brush_size = 5
# 현재 마우스로 그림을 그리고 있는 상태인지 확인하는 변수
drawing = False

# 마우스 이벤트를 처리하는 함수 정의
def paint(event, x, y, flags, param):
	# 전역 변수 drawing과 brush_size를 함수 안에서 사용하기 위해 선언
	global drawing, brush_size
	# 마우스 왼쪽 버튼을 눌렀을 때
	if event == cv.EVENT_LBUTTONDOWN:
		# 그림을 그리는 상태로 변경
		drawing = True
		# 해당 위치에 파란색 원을 그림 (BGR: 파랑=255,0,0)
		cv.circle(img, (x, y), brush_size, (255, 0, 0), -1)
	# 마우스 오른쪽 버튼을 눌렀을 때
	elif event == cv.EVENT_RBUTTONDOWN:
		# 그림을 그리는 상태로 변경
		drawing = True
		# 해당 위치에 빨간색 원을 그림 (BGR: 빨강=0,0,255)
		cv.circle(img, (x, y), brush_size, (0, 0, 255), -1)
	# 마우스를 이동했을 때 발생하는 이벤트
	elif event == cv.EVENT_MOUSEMOVE:
		# 현재 그림을 그리고 있는 상태일 경우
		if drawing:
			# 왼쪽 버튼을 누른 상태로 드래그할 경우
			if flags & cv.EVENT_FLAG_LBUTTON:
				# 파란색 원을 계속 그려서 드래그 그림 효과 생성
				cv.circle(img, (x, y), brush_size, (255, 0, 0), -1)
			# 오른쪽 버튼을 누른 상태로 드래그할 경우
			elif flags & cv.EVENT_FLAG_RBUTTON:
				# 빨간색 원을 계속 그려서 드래그 그림 효과 생성
				cv.circle(img, (x, y), brush_size, (0, 0, 255), -1)
	# 마우스 버튼을 놓았을 때 (왼쪽 또는 오른쪽)
	elif event == cv.EVENT_LBUTTONUP or event == cv.EVENT_RBUTTONUP:
		# 그림 그리기 상태 종료
		drawing = False

# "Paint"라는 이름의 창 생성
cv.namedWindow("Paint")
# 해당 창에서 마우스 이벤트 발생 시 paint 함수가 호출되도록 설정
cv.setMouseCallback("Paint", paint)

# 프로그램을 계속 실행하기 위한 무한 루프
while True:
	# 현재 이미지를 "Paint" 창에 출력
	cv.imshow("Paint", img)
	# 키보드 입력을 1ms 동안 대기 후 입력값을 가져옴
	key = cv.waitKey(1) & 0xFF
	# '+' 키를 누르면 붓 크기 증가
	if key == ord('+'):
		# 붓 크기를 1 증가시키되 최대값은 15로 제한
		brush_size = min(15, brush_size + 1)
		# 현재 붓 크기를 콘솔에 출력
		print("Brush size:", brush_size)
	# '-' 키를 누르면 붓 크기 감소
	if key == ord('-'):
		# 붓 크기를 1 감소시키되 최소값은 1로 제한
		brush_size = max(1, brush_size - 1)
		# 현재 붓 크기를 콘솔에 출력
		print("Brush size:", brush_size)
	elif key == ord('s'):
		save_path = os.path.join(script_dir, "paint_result.jpg")
		cv.imwrite(save_path, img)
		print("이미지가 저장되었습니다:", save_path)
	# 'q' 키를 누르면 프로그램 종료
	elif key == ord('q'):
		break
# 모든 OpenCV 창을 닫음
cv.destroyAllWindows()
```



# 주요 사용 함수 및 처리 흐름

- 풀이 방법 (흐름 설명)

- 초기화
	- 스크립트 기준으로 입력 이미지 경로를 정하고 `cv.imread()`로 로드
	- `brush_size = 5`, `drawing = False` 등 상태 변수 초기화
	- 윈도우 생성(`cv.namedWindow("Paint")`) 및 마우스 콜백 등록(`cv.setMouseCallback`)

- 마우스 콜백(상태 전이)
	- `EVENT_LBUTTONDOWN` / `EVENT_RBUTTONDOWN`: `drawing = True`, 클릭 위치에 즉시 원 그리기(좌=파랑, 우=빨강)
	- `EVENT_MOUSEMOVE`: `drawing == True`일 때 `flags`로 눌린 버튼 판별 후 `cv.circle()`로 연속 그리기
	- `EVENT_LBUTTONUP` / `EVENT_RBUTTONUP`: `drawing = False`

- 메인 루프
	- 화면 갱신: `cv.imshow("Paint", img)`
	- 키 처리: `key = cv.waitKey(1) & 0xFF`
		- `+` / `=`: `brush_size = min(15, brush_size+1)`
		- `-`: `brush_size = max(1, brush_size-1)`
		- `s`: 현재 캔버스 저장
		- `q`: 종료 전 최종 캔버스 저장(`results/painted_girl_laughing.png`) 후 루프 탈출

- 정리
	- `cv.imwrite()`로 파일 저장, `cv.destroyAllWindows()`로 윈도우 정리

유의사항
- 콜백 내부에서 전역 변수를 수정하므로 `global` 선언 필요
- `flags`는 비트마스크이므로 `flags & cv.EVENT_FLAG_LBUTTON`처럼 검사
- 성능: 큰 이미지를 실시간으로 그릴 때는 표시용 축소본을 사용하고, 최종 저장은 원본 크기로 수행

- `cv.setMouseCallback(window, callback)` — 마우스 이벤트 등록
- 마우스 이벤트 핸들러에서 `cv.EVENT_LBUTTONDOWN/UP`, `cv.EVENT_RBUTTONDOWN/UP`, `cv.EVENT_MOUSEMOVE` 처리
- `cv.circle(img, (x,y), radius, color, -1)` — 현재 브러시 크기로 원을 채워 그림
- `cv.waitKey(1)` 루프에서 키 처리: `+`/`=` → 크기 증가, `-` → 크기 감소, `q` → 종료

주의: 브러시 크기는 1~15 범위로 제한되어 있다.

# 실행

```powershell
cd Chapter_01
env\Scripts\python.exe E01_2.py
```
# 결과

![E01_2 preview](E01/E01_2.jpg)

---






