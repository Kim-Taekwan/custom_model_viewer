
## Overview

해당 프로젝트는 서울대학교 **컴퓨터그래픽스(4190.410)** 수업 과제의 결과물을 보강하여 만들어졌습니다.  
obj 파일로 모델을 지정하여 불러오고, Local Illumination Model 기반 셰이더를 적용하여 화면에 렌더링하는, 일련의 렌더링 파이프라인 작업을 수행하는 프로그램입니다.

## 설치 방법
다음과 같이 Pyglet 라이브러리를 설치합니다.

    pip install --upgrade --user pyglet

이후, 현재 리포지토리를 clone합니다.

    git clone https://github.com/Kim-Taekwan/custom_model_viewer.git

다음과 같이 코드를 실행합니다.

    python3 main.py

## 실행 및 조작 방법
프롬프트 상에서 원하는 모델의 번호를 입력하면, 다음 이미지와 같은 렌더링 창을 불러옵니다.

![image](https://github.com/Kim-Taekwan/custom_model_viewer/blob/main/Screenshots/Custom%20Model%20Viewer.png)

### 기본 조작
- 마우스 왼쪽 드래그 : 카메라 피벗 회전
- 마우스 휠 드래그 : 카메라 상하좌우 이동
- 마우스 휠 스크롤: 카메라 줌 인/아웃
- W/S/A/D : 카메라 앞/뒤/좌/우 이동
- E/Q : 카메라 상승/하강
- Space : 모델링 회전 토글
- Enter : 광원 회전 토글
- Esc : 프로그램 종료
### 셰이더 조작
![image](https://github.com/Kim-Taekwan/custom_model_viewer/blob/main/Screenshots/Genoge%20Miku%20-%20Texture%20Mode.png)
- 숫자 키 1 : Texture Mode (with Blinn-Phong Shading)
  - 해당 모델과 수동으로 매핑되어 있는 텍스쳐 파일을 불러와서 적용하는 모드입니다.
  - Ambient Occlusion(O), 노말 매핑(N), 툰 셰이딩(T) 텍스쳐가 매핑된 경우, 각 옵션의 ON/OFF 토글 기능을 지원합니다.

![image](https://github.com/Kim-Taekwan/custom_model_viewer/blob/main/Screenshots/Genoge%20Miku%20-%20Gouraud%20Illumination%20Mode.png)
- 숫자 키 2 : Gouraud Shading Mode
  - Gouraud Shading 사용: Vertex Shader로 색을 계산하는 모드입니다.
  - 모델을 구성하는 각 Vertex에서 Phong Illumination Model에 따라 색이 결정됩니다.

![image](https://github.com/Kim-Taekwan/custom_model_viewer/blob/main/Screenshots/Genoge%20Miku%20-%20Phong%20Illumination%20Mode.png)
- 숫자 키 3 : Phong Illumination Mode
  - Phong Shading 사용: Fragment(Pixel) Shader로 색을 계산하는 모드입니다.
  - 각 픽셀에서 Phong Illumination Model에 따라 색이 보간되어 결정됩니다.
 
![image](https://github.com/Kim-Taekwan/custom_model_viewer/blob/main/Screenshots/Genoge%20Miku%20-%20Blinn-Phong%20Illumination%20Mode.png)
- 숫자 키 4 : Blinn-Phong Illumination Mode
  - Phong Shading 사용: Fragment(Pixel) Shader로 색을 계산하는 모드입니다.
  - 각 픽셀에서 Blinn-Phong Illumination Model에 따라 색이 보간되어 결정됩니다.

![image](https://github.com/Kim-Taekwan/custom_model_viewer/blob/main/Screenshots/Rock(Wireframe).png)
- 숫자 키 5 : Wireframe Mode
  - 모델을 구성하는 Edge만을 보여주는 모드입니다.

## TODO
* 모델 불러오기 GUI 구현
* 모델 파일과 텍스쳐 파일 자동 매핑
* 실시간 셰이더 파라미터 조정
* Perlin Noise 기반 절차적 셰이더 생성

## 모델 출처
* [Free Rock](https://imolab-my.sharepoint.com/personal/jungdam_imo_snu_ac_kr/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fjungdam%5Fimo%5Fsnu%5Fac%5Fkr%2FDocuments%2FCourse%2FComputerGraphics%2FHW%2FFree%5Frock%2Ezip&parent=%2Fpersonal%2Fjungdam%5Fimo%5Fsnu%5Fac%5Fkr%2FDocuments%2FCourse%2FComputerGraphics%2FHW&ga=1)
* [Genoge Style Hatsune Miku](https://bowlroll.net/file/320915)
* [Sour Style Hatsune Miku](https://bowlroll.net/file/146103)
