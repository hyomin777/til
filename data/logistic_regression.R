# 이진 분류를 위해 3개의 범주를 보유한 iris의 Species를 두 개의 범주만 갖도록 도출
iris_bin1 <- subset(iris, Species == "setosa" | Species == "versicolor")
# 데이터 분할은 생략
str(iris_bin1)
# Species가 범주형(Factor) 변수로 setosa를 1로, versicolor를 2로 인식하고 있다.

# Species~.은 Species를 종속변수, 나머지 변수를 독립변수로 활용하겠다는 의미
# family = "binomial" glm을 로지스틱 회귀분석으로 사용하겠다는 의미
result <- glm(data = iris_bin1, Species ~ ., family = "binomial")
# "알고리즘이 수렴하지 않았습니다." 경고 문구는 control 값으로 조정가능
result <- glm(
  data = iris_bin1, Species ~ ., family = "binomial",
  control = list(maxit = 50)
)
# "적합된 확률 값들이 0 또는 1입니다." 경고 문구는 100%로 분류 가능을 의미

pairs(iris_bin1, col = iris_bin1$Species)
# 산점도에서 볼 수 있듯이 "setosa"와 "versicolor"는 Petal.Length와 Petal.Width에 의하여 완벽하게 분류될 수 있다.
# 따라서 Petal.Length와 Petal.Width가 독립변수로 포함되어 Species를 예측하고자 한다면 경고문구 "적합된 확률 값들이 0 또는 1입니다."를 계속해서 출력할 것이다.

result <- glm(
  data = iris_bin1, Species ~ Petal.Width, family = "binomial",
  control = list(maxit = 50)
)
result <- glm(
  data = iris_bin1, Species ~ Petal.Length, family = "binomial",
  control = list(maxit = 50)
)

# Petal.Length도 Petal.Width도 아닌 독립변수 활용
result <- glm(
  data = iris_bin1, Species ~ Sepal.Length, family = "binomial",
  control = list(maxit = 50)
)
summary(result)
# Null deviance: 절편만 포함한 모형의 완전 모형으로부터의 이탈도
# 값이 작을수록 완전 모형에 가깝다.
# Residual deviance: 독립변수들이 추가된 모형의 완전 모형으로부터의 이탈도
# 값이 작을수록 완전 모형에 가깝다.

# glm 함수를 활용한 로지스틱 회귀분석 결과는 p-value 값을 바로 알려주지 않는다.
# 따라서 p-value 값을 직접 구해서 모형의 기각 여부를 판단한다.
1 - pchisq(138.629, df = 99)
# p-value는 0.005302078로 유의수준 0.05하에서 기각
# 따라서 적합 결여 판정으로 절편만 포함한 모형은 완전모형에 가깝지 못하다.

1 - pchisq(64.211, df = 98)
# p-value는 0.9966935로 유의수준 0.05하에서 기각 불가
# 따라서 독립변수들이 포함된 모형은 완전모형에 가깝다.

# 즉, 위 모형이 관측된 자료를 잘 적합한다고 할 수 있다.
# 독립변수가 추가된 모형이 자료를 잘 설명하므로 각 계수에 대한 해석을 실시
# 절편(Intercept)에 대한 해석은 하지 않는다.
# Sepal.Length 회귀계수의 p-value가 3.28e-07로 유의수준 0.05보다 작다.
# 따라서 귀무가설 'H0: 회귀계수 = 0'을 기각
# Sepal.Length의 회귀계수 추정치는 5.140이다.
# Sepal.Length가 1 증가할 때 종속변수(y)가 1(setosa)에서 2(versicolor)일 확률이
# Odds 값이 exp(5.140) = 약 170배 증가함을 알 수 있다.
# Odds 값의 170배 증가는 versicolor일 확률이 170배 증가