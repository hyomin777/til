# 1. one sample t-test(일 표본 t-검정)
## 1. one sample t-test의 개념
- one sample t-test는 가설검정의 일종으로, 하나의 모집단의 평균(n)값을 특정값과 비교하는 경우 사용하는 통계적 분석 방법이다.

## 2. 일 표본 단측 t-검정
- 모수에 대한 검정을 할 때 모수값이 `~보다 크다` 혹은 `~보다 작다`와 같이 한쪽으로의 방향성을 갖는 경우 수행되는 검정 방법이다.
- 예컨대 `OO공장에서 생산되는 지우개의 평균 중량은 50g 이하다(지우개 평균 중량 $\leq$50g)`라는 귀무가설을 수립했다고 가정해보자.
- 다음과 같이 R에서 t-검정을 수행할 수 있다.
```
> weights <- runif(10, min = 49, max = 52)
> t.test(weights, mu = 50, alternative = "greater")
        One Sample t-test
data:  weights
t = 2.9298, df = 9, p-value = 0.008382
alternative hypothesis: true mean is greater than 50
95 percent confidence interval:
 50.24834      Inf
sample estimates:
mean of x
 50.66346
```
- 결과를 보면 검정통계량은 t = 2.9298이며, 자유도는 표본의 개수보다 1만큼 적은 df = 9이다.
- p-value가 유의수준 0.05보다 작으므로 귀무가설을 기각할 수 있다.
- 따라서 귀무가설은 기각되고 대립가설인 `OO공장에서 생산되는 지우개의 평균 중량은 50g 보다 크다`라는 대립가설을 채택한다.

## 3, 일 표본 양측 t-검정
- 단측 검정처럼 방향성을 갖지 않고 모수값이 `~이다` 혹은 `~이 아니다`와 같이 방향성이 없는 경우 수행되는 검정 방법이다.
- 예컨대 `대한민국 남성의 평균 몸무게는 70kg이다(대한민국 남성 평균 몸무게 = 70kg)`이라는 귀무가설을 수립했다고 가정해보자.
- 다음과 같이 R에서 t-검정을 수행할 수 있다.
```
> weights <- runif(100, min = 40, max = 100)
> t.test(weights, mu = 70, alternative = "two.sided")
        One Sample t-test
data:  weights
t = -0.036805, df = 99, p-value = 0.9707
alternative hypothesis: true mean is not equal to 70
95 percent confidence interval:
```
- 결과를 보면 검정통계량 t = -0.036805이며, 자유도는 표본의 개수보다 1만큼 적은 df = 99이다.
- p-value가 유의수준 0.05보다 작지 않으므로 귀무가설을 기각할 수 없다.
- 따라서 `대한민국 남성의 평균 몸무게는 70kg이다`라는 귀무가설은 기각되지 않고 채택된다.

