## 1. Introduction
* **Dataset Name:** Smartphone-Based Recognition of Human Activities and Postural Transitions Data Set (HAPT)  
* **Source:** UCI Machine Learning Repository  
* **Objective:** 인간의 기본 활동(Basic Activities)뿐만 아니라, 자세가 변화하는 **전이 구간(Postural Transitions)**을 명확히 식별하기 위해 구축된 데이터셋.  
* **Participants:** 30명의 자원자 (19–48세)  
* **Sampling Rate:** 50 Hz  

## 2. Sensor Placement & Modalities
피험자들은 허리(Waist)에 스마트폰(Samsung Galaxy S II)을 착용한 상태로 실험을 수행.  
* **Device:** Smartphone (Samsung Galaxy S II) attached on the waist.  
* **Sensors:**  
    * **3-axial Accelerometer** (3축 가속도; 중력/신체 성분이 섞인 가속도 신호를 측정하며, RawData에서는 두 성분이 분리된 형태로 제공되지는 않음)  
    * **3-axial Gyroscope** (Tri-axial Angular Velocity)  
* **Pre-processing:** README 기준으로, 561차원 feature 벡터를 생성할 때는 센서 신호에 median filter와 20 Hz 저역 통과 Butterworth filter를 적용한 뒤, 2.56초(128 samples), 50% overlap의 슬라이딩 윈도우로 나누어 time/frequency domain feature를 계산함. HAPT v2에서는 이와 별도로, **원시 관성 신호(raw inertial signals)와 frame-level activity labels**를 `RawData/` 디렉터리로 제공하며, 중력 가속도(Gravity)와 신체 가속도(Body Acceleration)의 분리 신호는 RawData 파일에 포함되지 않고 feature 수준에서만 정의됨.

## 3. Activity List (12 Classes)
이 데이터셋의 가장 큰 특징은 **6가지 기본 동작** 외에, 자세가 바뀌는 **6가지 전이(Transition) 동작**이 별도의 클래스로 레이블링되어 있다는 점.

### A. Basic Activities (Static & Dynamic)
1. **WALKING**  
2. **WALKING_UPSTAIRS**  
3. **WALKING_DOWNSTAIRS**  
4. **SITTING**  
5. **STANDING**  
6. **LAYING**

### B. Postural Transitions (Target of Interest)
이 구간들은 짧은 지속 시간(Short duration)을 가지며, 동작 간의 연결 고리 역할을 함.  
7. **STAND_TO_SIT** (서기 → 앉기)  
8. **SIT_TO_STAND** (앉기 → 서기)  
9. **SIT_TO_LIE** (앉기 → 눕기)  
10. **LIE_TO_SIT** (눕기 → 앉기)  
11. **STAND_TO_LIE** (서기 → 눕기)  
12. **LIE_TO_STAND** (눕기 → 서기)

## 4. Data Structure
데이터셋은 Raw Data 파일과 정답지(Label) 파일이 분리되어 제공됨.

### Raw Data Files
* **Path:** `RawData/`  
* **Naming Convention:**  
  - `acc_expXX_userYY.txt` (Accelerometer)  
  - `gyro_expXX_userYY.txt` (Gyroscope)  
    * `XX`: Experiment ID (실험 번호)  
    * `YY`: User ID (피험자 번호)  
* **Format:** 공백으로 구분된 3축 데이터 (X, Y, Z). 각 row는 50 Hz로 샘플링된 하나의 센서 측정값을 의미함.

### Ground Truth Labels (`labels.txt`)
전이 구간을 포함한 모든 동작의 시작과 끝이 프레임 단위로 명시.  
* **Format:** `[Experiment ID] [User ID] [Activity ID] [Start Point] [End Point]`  
* **Example:**
    ```text
    1  1  5  1    250   (User 1, Exp 1, Act 5(Standing), Frame 1~250)
    1  1  7  251  300   (User 1, Exp 1, Act 7(Stand_to_Sit), Frame 251~300)
    ```

## 5. Key Characteristics for Research
* **Explicit Transition Labels:** 대부분의 HAR 데이터셋이 전이 구간을 'Null' 클래스나 노이즈로 처리하는 것과 달리, HAPT는 이를 명확한 클래스(ID 7~12)로 정의하고 있어 **전이 탐지(Transition Detection) 알고리즘의 평가를 위한 Ground Truth**로 활용하기에 최적.
* **Unsupervised Learning Benchmark:** 모든 Raw time-series는 frame-level GT가 완비되어 있으나, 전이 구간이 매우 짧고 패턴 변화가 뚜렷해 비지도 학습 기반의 **Change Point Detection (CPD)** 및 **Segmentation 연구**에 적합.
