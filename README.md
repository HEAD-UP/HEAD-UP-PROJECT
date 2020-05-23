# HEAD-UP-PROJECT
## 사각지대 위험 인식 프로그램
### 참여인원
- 멘토 : 김정석 (소속 : SKT)   
- 멘티 : 김준영, 김형진, 박주홍, 심재욱 (소속 : 경북대학교 컴퓨터학부)   
- 담당교수 : 고석주 (소속 : 경북대학교 컴퓨터학부)

---

### 목표 및 내용
◯ 목표
- 2대의 카메라를 사용하여 자동차와 사람을 인식하고 이동경로를 알 수 있게 한다. 
- 자동차와 자동차 간의 충돌, 자동차와 사람 간의 충돌을 예상한다.
- 충돌이 예상될 경우 신호를 실시간으로 전송하여 외부로 송출하여 충돌을 예방한다.

◯ 2대의 카메라를 사용하여 스트리밍 영상의 시간을 동기화한다.
- 먼저 유선 연결된 2대의 카메라의 영상을 동기화한다.
- 이 후, 2대의 카메라에서 무선으로 전송되는 영상을 동기화한다.

◯ Object Detection 과 Object Tracking 을 통해 자동차와 사람을 인식하고, 이동경로를 파악한다.
- Tensorflow 와 SORT 알고리즘을 활용한다.
- Amazon 의 AWS Rekognition API를 활용한다.
- Tracking 시에 소요되는 계산량이 너무 많을 경우, 객체의 중심점으로부터 유클리디안 거리를 계산하여 움직임을 확인한다.
- 이 때 사용되는 영상은 녹화된 영상, 유선 스트리밍 영상, 무선 스트리밍 영상 순으로 테스트한다.

◯ 서버에서 송신된 신호를 외부로 나타낸다.
- 최종적으로는 핸드폰에 그 신호를 띄우는 것이 목표지만 프로젝트의 완성도를 위해 단순히 LED 등을 사용하여 수신된 신호를 표현하는 것을 목표로 한다.

---

### 다이어그램

#### 시스템 개요도
<img src="/문서 자료/사진자료/system_planning_diagram.png"></img>

#### 시스템 다이어그램
<img src="/문서 자료/보고서/XML 자료/BOX_HEAD_01.jpg"></img>

#### 엑티비티 다이어그램
<img src="/문서 자료/보고서/XML 자료/BOX_HEAD_ACTIVITY_DIAGRAM.jpg"></img>

---

### 샘플 상황

#### 카메라 1이 자동차를 인식 - 카메라 2가 자동차를 인식
<img src="/문서 자료/보고서/XML 자료/SITUATION_CAR_CAR.jpg"></img>

#### 카메라 1이 자동차를 인식 - 카메라 2가 사람을 인식
<img src="/문서 자료/보고서/XML 자료/SITUATION_CAR_PERSON.jpg"></img>

#### 카메라 1이 사람을 인식 - 카메라 2가 자동차를 인식
<img src="/문서 자료/보고서/XML 자료/SITUATION_PERSON_CAR.jpg"></img>


---

### 사용된 재료
- 라즈베리파이4 키트 (Raspberry pi4 Kit) 2개
[라즈베리파이 opencv 사용]
- 라즈베리파이 카메라 케이스 (Raspberry Pi Camera Board Case with 1/4" Tripod Mount) 2개
[카메라 케이스]
- 라즈베리파이 카메라 V2 (V2) 2개
[라즈베리파이 영상 인식 카메라]
- 변환커넥터 (HDMI to DVI) 2개 
[라즈베리파이 모니터 잭 변환 커넥터]
- 라즈베리파이LED (3색 RGB LED 모듈 라즈베리파이) 2개
[라즈베리파이 알림용 LED]


---

### 서버 JSON 파싱 결과
<img src="/문서 자료/사진자료/server_result_200419.png"></img>

---

### Install Method (Internet Connection needed)
0. use raspberry pi imager and make OS file in SD card
1. install raspbian OS in raspberry pi (We use Raspberry PI 4 and Raspbian GNU/Linux 10)
2. open terminal and type "git clone https://github.com/HEAD-UP/HEAD-UP-PROJECT.git"
3. copy "install" file contents("update_env.sh", "install_lib_env.sh", "tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl") into raspberry root (normally "/home/pi")
4. type "./install_lib_env.sh" in terminal
5. type "reboot" in terminal
6. open terminal and type "./install_lib_env.sh" in terminal (it takes a long time)
7. click start button in raspbian OS, and preferences -> Raspberry Pi Configuration -> Interfaces
8. Set camera Disable to Enable and close the Raspberry Pi Configuration window
9. type "reboot" in terminal
10. open terminal and type "jupyter notebook"