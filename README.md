
## Overview

해당 프로젝트는 서울대학교 **컴퓨터그래픽스(4190.410)** 수업 과제의 결과물을 보강하여 만들어졌습니다.  
obj 파일로 모델을 지정하여 불러오고, local illumination model 기반 셰이더를 적용하여 화면에 렌더링하는, 일련의 렌더링 파이프라인 작업을 수행하는 프로그램입니다.

## 설치 방법
다음과 같이 Pyglet 라이브러리를 설치합니다.

    pip install --upgrade --user pyglet

이후, 현재 리포지토리를 clone합니다.

    git clone https://github.com/Kim-Taekwan/custom_model_viewer.git

다음과 같이 코드를 실행합니다.

    python3 main.py

## 실행 및 조작 방법
원하는 모델의 번호를 입력하면, 다음과 같이 렌더링 창을 불러옵니다.

### 기본 조작
- 마우스 왼쪽 드래그 : 카메라 피벗 회전
- 마우스 가운데 드래그 : 카메라 상하좌우 이동
- W/S/A/D : 카메라 앞/뒤/좌/우 이동
- E/Q : 카메라 상승/하강
- 스페이스 : 모델링 회전 토글
### 셰이더 조작
- 숫자 키 1 : Texture Mode (with Blinn-Phong Shading)
- 숫자 키 2 : Gouraud Illumination Mode
- 숫자 키 3 : Phong Illumination Mode
- 숫자 키 4 : Blinn-Phong Illumination Mode
- 숫자 키 5 : Wireframe Mode

## TODO
* 모델 불러오기 GUI 구현
* 모델 파일과 텍스쳐 파일 자동 매핑
* 실시간 셰이더 파라미터 조정
