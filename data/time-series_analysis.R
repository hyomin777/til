library(datasets)
library(forecast)
auto.arima(Nile)
# ARIMA(1, 1, 1) 모형이 적절하다고 판단
# ARIMA(1, 1, 1) 모형으로 Nile 데이터 모형 구축
result <- arima(Nile, order = c(1, 1, 1))
# 구축된 모형으로 미래 5년 예측
pred <- forecast(result, h = 5)
pred
# Forecast는 예측 평균값
# 내년 유입량의 80% 신뢰 구간은 Lo 80과 Hi 80인 635.9909와 996.3717 사이
# 내년 유입량의 95% 신뢰 구간은 Lo 95와 Hi 95인 540.6039와 1091.759 사이

# 예측 데이터 시각화
plot(pred)