# 시계열 자료의 정상성 조건
# 1. 일정한 평균

# 2018년 1월부터 2019년 12월까지 매월 초의 환율 데이터
rate <- c(
  1072, 1081, 1090, 1065, 1087,
  1085, 1130, 1130, 1122, 1122,
  1144, 1121, 1131, 1129, 1137,
  1146, 1176, 1194, 1174, 1200,
  1224, 1213, 1172, 1197
)
plot(rate, type = "l")
# 평균이 일정하지 않다. 즉 정상성에 위배된다.
# 따라서 1회 차분을 실시한다.

rate_diff <- diff(rate, lag = 1)
plot(rate_diff, type = "l")
# 1회 차분 결과 평균이 일정해지는 것을 확인할 수 있다.

# 2. 일정한 분산
# R 내장 시계열 데이터인 UKgas 활용
plot(UKgas)
# 시간의 흐름에 따라 분산이 일정하지 않다고 판단되어 정상성을 위배
# 따라서 자연 log를 취하여 변환을 실시한다.

UKgas_log <- log(UKgas)
plot(UKgas_log)
# 변환을 실시함으로써 분산이 일정해지는 것을 확인할 수 있다.

# 3. 시차에만 의존하는 공분산
# 임의의 시계열 데이터 생성
data <- rnorm(100)
# 시차를 3으로 설정
diff <- 3
x <- 1 : (100 - diff)
y <- x + diff
# 시차를 3으로 갖는 시계열 자료의 산점도
plot(data[x], data[y])
# 특정 시점이 아닌 시차에 영향을 받는 공분산 값
cov(data[x], data[y])