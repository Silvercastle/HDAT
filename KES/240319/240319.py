import tensorflow.compat.v1 as tf  # TensorFlow 1.x 버전을 사용하기 위해 호환성 모듈을 불러옵니다.
tf.disable_v2_behavior()  # TensorFlow 2.x의 기능을 사용하지 않도록 설정합니다.

xData = [1,2,3,4,5,6,7]  # 입력 데이터
yData = [25000,55000,75000, 110000, 128000, 155000, 180000]  # 출력 데이터

W = tf.Variable(tf.random.uniform([1], -100, 100))  # Weight를 랜덤 초기화합니다.
b = tf.Variable(tf.random.uniform([1], -100, 100))  # Bias를 랜덤 초기화합니다.
X = tf.placeholder(tf.float32)  # 입력값을 담을 Placeholder를 생성합니다.
Y = tf.placeholder(tf.float32)  # 출력값을 담을 Placeholder를 생성합니다.
H = W * X + b  # 가설 함수를 정의합니다: H = W*X + b
cost = tf.reduce_mean(tf.square(H-Y))  # 손실 함수를 정의합니다: 평균 제곱 오차
a = tf.Variable(0.01)  # 학습률을 설정합니다.

optimizer = tf.train.GradientDescentOptimizer(a)  # Gradient Descent Optimizer를 정의합니다.
train = optimizer.minimize(cost)  # 최적화 과정을 정의합니다: 손실 함수를 최소화하는 방향으로 학습합니다.
init = tf.global_variables_initializer()  # 변수들을 초기화하기 위한 연산을 정의합니다.

sess = tf.Session()  # 세션을 생성합니다.
sess.run(init)  # 변수들을 초기화합니다.

for i in range(5001):  # 5000번의 반복 학습을 수행합니다.
    sess.run(train, feed_dict={X: xData, Y: yData})  # 학습 연산을 실행하고 입력과 출력 데이터를 전달합니다.
    if i % 500 == 0:  # 500번의 학습마다 현재 손실값과 파라미터(W, b)를 출력합니다.
        print(i, sess.run(cost, feed_dict={X: xData, Y: yData}), sess.run(W), sess.run(b))

print(sess.run(H, feed_dict={X: [8]}))  # 학습된 모델을 통해 새로운 입력값에 대한 예측을 출력합니다.

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.DataFrame({'time': xData, 'price': yData})
print(df)

import numpy as np
from statsmodels.formula.api import ols
z=np.polyfit(df['time'], df['price'], 1) # 기울기와 절편 확인
f=np.poly1d(z) # f(x): f함수에 x값을 넣으면 y값을 계산해 줌
print(z[0], z[1])
print(f(1))
#statsmodel을 통해 회귀식의 회귀계수(기울기, 절편) 확인
ols('price ~ time', data=df).fit().summary()

plt.rcParams["figure.figsize"] = (12,6)
sns.regplot(x='time', y='price', data=df)
plt.xlim(df['time'].min(), df['time'].max()+5)
plt.ylim(df['price'].min(), df['price'].max()+100000)
plt.text(5, 230000, "y = %fx + %f" %(z[0], z[1]), color="#005599")
plt.grid()
plt.show()