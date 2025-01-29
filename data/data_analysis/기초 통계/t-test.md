# 1. one sample t-test(일 표본 t-검정)
## 1. one sample t-test의 개념
- one sample t-test는 가설검정의 일종으로, 하나의 모집단의 평균(n)값을 특정값과 비교하는 경우 사용하는 통계적 분석 방법이다.

## 2. 일 표본 단측 t-검정
- 모수에 대한 검정을 할 때 모수값이 `~보다 크다` 혹은 `~보다 작다`와 같이 한쪽으로의 방향성을 갖는 경우 수행되는 검정 방법이다.
- 예컨대 'OO공장에서 생산되는 지우개의 평균 중량은 50g 이하다(지우개 평균 중량 $\leq$50g)'라는 귀무가설을 수립했다고 가정해보자.
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

# 2. independent sample t-test(이(독립) 표본 t-검정)
## 1. 이 표본 t-검정의 개념
- 이 표본 t-검정은 가설검정의 일종으로 서로 독립적인 두 개의 집단에 대하여 모수(모평균)의 값이 같은 값을 갖는지 통계적으로 검정하는 방법이다.
- 여기서 독립이란 두 모집단에서 각각 추출된 두 표본이 서로 관계가 없다는 것을 의미한다.
- 두 모집단의 분산이 같음을 의미하는 등분산성을 만족해야 한다.
- 따라서 독립 표본 t-검정을 수행하기 전에 등분산 검정(F 검정)을 먼저 수행해야 한다.

## 2. 이 표본 단측 t-검정
- 두 집단에 대하여 모수 비교를 할 때 `~이 ~보다 크다` 혹은 `~이 ~보다 작다`와 같이 두 집단 사이에 대소가 있는 경우 수행되는 검정 방법이다.
- 예컨대 'A회사의 급여가 B회사의 급여보다 같거나 많다(A회사 급여 $\geq$ B회사 급여)'라는 귀무가설을 수립했다고 가정해보자.
```
> salaryA <- runif(100, min = 250, max = 380)
> salaryB <- runif(100, min = 200, max = 400)
> t.test(salaryA, salaryB, alternative = "less")
        Welch Two Sample t-test
data:  salaryA and salaryB
t = 1.3204, df = 159.54, p-value = 0.9057
alternative hypothesis: true difference in means is less than 0
95 percent confidence interval:
    -Inf 21.0059
sample estimates:
mean of x mean of y
 311.5856  302.2620
```
- 검정통계량 t = 1.3204, 자유도 df = 159.54이다.
  - 만약 등분산(var.equal = True) 가정을 하게되면 자유도는 전체 데이터 수(200) - 2 =198이 된다.
- p-value가 0.9057이며, 유의수준 0.05보다 크므로 귀무가설을 기각할 수 없다.
- 따라서 A회사의 급여가 B회사의 급여보다 같거나 많다고 할 수 있다.

## 3. 이 표본 양측 t-검정
- 두 집단에 대하여 모수 비교를 할 때 `두 집단이 같다` 혹은 `두 집단이 다르다`와 같이 두 집단 사이에 대소가 없는 경우 수행되는 검증 방법이다.
- 예컨대 `K와 L의 달리기 속도는 같다(K의 달리기 속도 = L의 달리기 속도)`라는 귀무가설을 수립했다고 가정해보자.
```
> speedK <- runif(100, min = 30, max = 40)
> speedL <- runif(100, min = 25, max = 35)
> t.test(speedK, speedL, alternative = "two.sided")
        Welch Two Sample t-test
data:  speedK and speedL
t = 10.975, df = 197.93, p-value < 2.2e-16
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
 3.707675 5.331922
sample estimates:
mean of x mean of y
 34.65502  30.13522
```
- 검정통계량 t = 10.975, 자유도 df = 197.93이다.
  - 만약 등분산(var.equal = TRUE) 가정을 하게 되면 자유도는 전체 데이터 수(200) - 2 = 198이 된다.
- p-value < 2.2e-16으로 유의수준 0.05보다 작으므로 귀무가설을 기각할 수 있다.
- 따라서 대립가설을 채택하여 K와 L의 달리기 속도는 같다고 할 수 없다.

# 3. paired t-test(대응 표본 t-검정)
## 1. 대응 표본 t-검정의 개념
- 동일한 대상에 대해 두 가지 관측치가 있는 경우 이를 비교하여 차이가 있는지 검정할 때 사용한다.
- 주로 실험 전후의 효과를 비교하기 위해 사용한다.
  - 두 집단에 신약 투약 이후의 전후 수치 비교
  - 새로운 정책이 시행된 후의 부동산 가격의 전후 변화 등

## 2. 대응 표본 t-검정
- 예를 들어 새로운 운동법이 체중감량의 효과가 있는지 검증하기 위해 새로운 운동법을 실시한 집단과 실시하지 않은 집단의 체중을 비교한다고 했을 때 대응 표본 t-검정을 수행한다.
- '새로운 운동법으로 체중 감량의 효과는 없다(운동 전 무게 - 운동 후 무게 $\leq$ 0)'라는 귀무가설을 수립하고 R에서 t-검정을 수행했다.
```
> before <- runif(100, min = 60, max = 80)
> after <- before + rnorm(100, mean = -3, sd = 2)
> t.test(before, after, alternative = "greater", paired = TRUE)
        Paired t-test
data:  before and after
t = 16.216, df = 99, p-value < 2.2e-16
alternative hypothesis: true mean difference is greater than 0
95 percent confidence interval:
 2.917578      Inf
sample estimates:
mean difference
       3.250388
```
- 검정통계량 t = 16.216, 자유도 df = 99
- p-value < 2.2e-16으로 유의수준 0.05보다 작으므로 귀무가설을 기각할 수 있다.