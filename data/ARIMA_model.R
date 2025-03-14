# 2018년 1월부터 2019년 12월까지 매월 초의 환율 데이터
rate <- c(
  1072, 1081, 1090, 1065, 1087, 1085,
  1130, 1130, 1122, 1122, 1144, 1121,
  1131, 1129, 1137, 1146, 1176, 1194,
  1174, 1200, 1224, 1213, 1172, 1197
)
# 수치형 벡터를 시계열 자료로 변환
rate_ts <- ts(rate)
# forecast 패키지에 내장되어 있는 auto.arima 함수를 사용하여 최적의 모형을 구할 수 있다.
install.packages("xts")
install.packages("forecast")
library(forecast)
# 최적의 모형을 선정
auto.arima(rate_ts)
# 최적의 모형은 정상성 만족을 위해 1회의 차분이 필요한 ARIMA(0, 1, 0)이다.

# 1회의 차분을 진행한 뒤 자기상관함수와 부분자기상관함수를 확인해보자.
rate_ts_diff1 <- diff(rate_ts, differences = 1)

acf(rate_ts_diff1)
pacf(rate_ts_diff1)
# 두 그래프 모두 시차가 1인 지점에서 처음으로 파란선 안에 존재
# 즉 시차가 1인 지점부터 자기상관이 낮음
# 시차가 1, 즉 바로 이전 시점이 현재 시점에 영향을 주지 않는다고 판단 가능
# 1회 차분시 AR(0), MA(0)이 되는 것을 확인할 수 있다.
# 결론적으로 1회 차분하여 정상성을 만족하는 자료는 이전 시점에 영향을 받지 않는 무작위 변동이라고 판단할 수 있다.
# 2년간 24개의 자료가 아닌 더 많은 데이터를 보유하고 있다면 다른 결과가 나올 수 있다.