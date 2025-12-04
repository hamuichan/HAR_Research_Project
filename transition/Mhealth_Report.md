## 1. Introduction
* **Dataset Name:** mHealth (Mobile Health) Dataset
* **Source:** UCI Machine Learning Repository
* **Objective:** 신체 모니터링 및 인간 행동 인식(HAR)을 위한 다중 모달 센서 데이터셋
* **Participants:** 10명의 자원자 (다양한 신체 프로필 보유)
* **Sampling Rate:** 50 Hz

## 2. Sensor Placement & Modalities
데이터는 신체의 3개 부위에 부착된 웨어러블 센서(Shimmer2BURST)를 통해 수집됨. 총 23개의 속성(Column)을 가짐.

| Sensor Location | Included Sensors | Modalities | 비고 |
| :--- | :--- | :--- | :--- |
| **Chest (가슴)** | Accelerometer, ECG | 2-lead ECG, 3-axis Acc | **Gyroscope 없음** |
| **Left Ankle (왼쪽 발목)** | Accelerometer, Gyroscope, Magnetometer | 3-axis Acc, Gyro, Mag | |
| **Right Lower Arm (오른쪽 아래 팔)** | Accelerometer, Gyroscope, Magnetometer | 3-axis Acc, Gyro, Mag | |

> **Note:** 가슴(Chest) 센서에는 각속도계(Gyroscope)가 포함되어 있지 않으므로, 상체 회전 동작 분석 시 가속도계(Accelerometer) 데이터에 의존해야 할 것 같음.

## 3. Data Structure
각 피험자(Subject)별로 별도의 로그 파일(`mHealth_subject1.log` ~ `mHealth_subject10.log`)로 구성

### Column Mapping (Total 23 Columns + Label)
* **Column 0-2:** Acceleration from the chest sensor (X, Y, Z)
* **Column 3-4:** ECG signal (Lead 1, Lead 2)
* **Column 5-7:** Acceleration from the left ankle sensor (X, Y, Z)
* **Column 8-10:** Gyro from the left ankle sensor (X, Y, Z)
* **Column 11-13:** Magnetometer from the left ankle sensor (X, Y, Z)
* **Column 14-16:** Acceleration from the right lower arm (X, Y, Z)
* **Column 17-19:** Gyro from the right lower arm (X, Y, Z)
* **Column 20-22:** Magnetometer from the right lower arm (X, Y, Z)
* **Column 23:** Activity Label (Class ID)

## 4. Activity List
피험자들은 각 동작을 약 1분간 수행하였으며, 데이터셋에는 총 12가지의 신체 활동이 포함. (Label 0은 Null class/No activity로 간주)

1. Standing still (1 min)
2. Sitting and relaxing (1 min)
3. Lying down (1 min)
4. Walking (1 min)
5. Climbing stairs (1 min)
6. Waist bends forward (20x) 
7. Frontal elevation of arms (20x)
8. Knees bending (Crouching) (20x) 
9. Cycling (1 min)
10. Jogging (1 min)
11. Running (1 min)
12. Jump front & back (20x) 

## 5. Key Characteristics
* **Multi-modal:** 가속도, 자이로, 지자계, 심전도(ECG) 데이터를 모두 포함하여 다양한 센서 융합 연구 가능.
* **Repetitive Actions:** Activity 6, 7, 8, 12번은 명확한 횟수(20회)를 가진 반복 동작으로, 카운팅(Counting) 및 세그멘테이션(Segmentation) 연구에 적합함.
* **Realistic Constraints:** 실제 헬스케어 환경을 고려하여 센서 부착 위치가 선정되었으며, 센서별 가용 데이터(Chest에 Gyro 부재 등)의 차이가 존재함.