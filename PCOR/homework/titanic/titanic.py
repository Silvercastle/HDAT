import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# 훈련, 테스트, 제출 데이터의 파일 경로
path = 'Z:/VS Project/HDAT/PCOR/homework/titanic/data/'
data = pd.read_csv(path + 'train.csv')  # 훈련 데이터를 불러옵니다
data1 = pd.read_csv(path + 'test.csv')  # 테스트 데이터를 불러옵니다
data2 = pd.read_csv(path + 'submission.csv')  # 예측 결과와 비교할 제출 파일을 불러옵니다

# 데이터 전처리
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']  # 사용할 특성 열을 정의합니다
target = 'Survived'  # 목표 열을 정의합니다

# 훈련 데이터 준비
X_train = data[features]  # 훈련용 특성을 추출합니다
y_train = data[target]  # 훈련용 타겟 변수를 추출합니다

# 수치형 및 범주형 데이터에 대한 전처리 파이프라인
numeric_features = ['Age', 'SibSp', 'Parch', 'Fare']  # 수치형 특성 열 목록
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),  # 열의 중앙값으로 결측값을 채웁니다
    ('scaler', StandardScaler())])  # 표준화를 통해 특성을 스케일링합니다

categorical_features = ['Pclass', 'Sex', 'Embarked']  # 범주형 특성 열 목록
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),  # 결측값을 'missing'으로 채웁니다
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])  # 범주형 데이터를 원-핫 인코딩 벡터로 변환합니다

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),  # 수치형 특성에 수치형 변환기 적용
        ('cat', categorical_transformer, categorical_features)])  # 범주형 특성에 범주형 변환기 적용

# 훈련 데이터를 핏하고 변환합니다
X_train_preprocessed = preprocessor.fit_transform(X_train)  # 훈련 데이터를 처리합니다
y_train = y_train.values  # 모델 훈련을 위해 타겟 데이터를 numpy 배열로 변환합니다

# 테스트 데이터 준비
X_test = data1[features]  # 테스트 데이터에서 특성을 추출합니다
X_test_preprocessed = preprocessor.transform(X_test)  # 테스트 데이터를 처리합니다

# 모델 생성: Sequential 모델을 사용하여 신경망 모델을 구성합니다.
model = Sequential([
    # 첫 번째 은닉층: 64개의 뉴런을 가지고 활성화 함수는 ReLU를 사용하며, 입력 형태는 X_train_preprocessed.shape[1]입니다.
    Dense(64, activation='relu', input_shape=(X_train_preprocessed.shape[1],), kernel_regularizer=l2(0.001)),
    Dropout(0.3),  # 과적합을 방지하기 위해 30%의 뉴런을 무작위로 드롭아웃합니다.
    # 두 번째 은닉층: 32개의 뉴런을 가지고 활성화 함수는 ReLU를 사용합니다. L2 정규화가 적용되어 가중치를 제한합니다.
    Dense(32, activation='relu', kernel_regularizer=l2(0.001)),
    Dropout(0.3),
    # 세 번째 은닉층: 16개의 뉴런을 가지고 활성화 함수는 ReLU를 사용합니다. L2 정규화가 적용되어 가중치를 제한합니다.
    Dense(16, activation='relu', kernel_regularizer=l2(0.001)),
    Dropout(0.3),
    # 출력층: 이진 분류를 위한 시그모이드 활성화 함수를 사용합니다.
    Dense(1, activation='sigmoid')
])

# 옵티마이저: Adam, 학습률을 점진적으로 감소시키는 스케줄러 적용
optimizer = Adam(learning_rate=0.001)

model.compile(optimizer=optimizer,
              loss='binary_crossentropy',
              metrics=['accuracy']) # 모델을 아담 옵티마이저와 이진 크로스엔트로피 손실 함수를 사용하여 컴파일합니다

# 모델 훈련
model.fit(X_train_preprocessed, y_train, epochs=50, batch_size=32, validation_split=0.2)  # 50 에포크 동안 모델을 훈련합니다

# 테스트 세트에 대한 예측 생성
predictions = model.predict(X_test_preprocessed)  # 처리된 테스트 데이터를 사용하여 예측합니다
predictions = (predictions > 0.5).astype(int).reshape(-1)  # 확률을 이진 예측으로 변환합니다

# 제출 파일을 불러와 예측 결과와 비교합니다
true_labels = data2['Survived'].values  # 제출 파일에서 실제 레이블을 추출합니다

# 제공된 제출 파일을 기준으로 모델의 정확도를 평가합니다
accuracy = accuracy_score(true_labels, predictions)  # 예측의 정확도를 계산합니다
print(f"Accuracy of the model on the test set is: {accuracy}")  # 정확도를 출력합니다
