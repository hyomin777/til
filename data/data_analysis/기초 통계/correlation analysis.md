# 1. 상관분석의 개념
## 1. 상관분석의 개념
- 상관분석은 두 변수 간의 선형적 관계가 존재하는지 알아보는 분석 방법으로, 상관계수를 활용한다.
- 상관계수는 -1과 +1 사이의 값을 갖는데, +1에 가까우면 강한 양의 상관관계가, -1에 가까우면 강한 음의 상관관계가 있다고 본다. 0에 가까울수록 상관관계가 존재하지 않는다고 본다.
- 변수 간에 상관관계가 있다는 것이 반드시 그 변수들 사이에 인과관계가 있다는 말은 아니다. 상관관계는 존재하지만 인과관계는 없을 수도 있다.

## 2. 산점도 행렬
- R에서 산점도 행렬(Scatter Plot Matrix)을 그려 여러 변수를 조합한 산점도와 상관계수를 한 화면에서 확인할 수 있다.

## 3. 상관분석 귀무가설
- 상관분석의 귀무가설은 '$H_0: \gamma_{xy} = 0$(두 변수는 아무 상관관계가 없다.)'이다.
- p-value가 유의수준보다 작아 귀무가설을 기각할 수 있다면 두 변수 간에 유의한 상관관계가 있다고 말할 수 있다.

# 2. 상관분석의 종류
## 1. 피어슨 상관분석(선형적 상관관계)
- 피어슨 상관계수는 모수적 방법의 하나로 두 변수가 모두 정규분포를 따른다는 가정이 필요하다.
$$
\gamma_{xy}=\frac{\sum^n_i(X_i-\bar{X})(Y_i-\bar{Y})}{\sqrt{\sum^n_i(X_i-\bar{X})^2}\sqrt{\sum^n_i(Y_i-\bar{Y})^2}}
$$

```
> X <- c(1, 2, 3, 4, 5)
> Y <- c(3, 6, 4, 9, 8) 
> cor(X, Y, method = 'pearson')
[1] 0.8062258
```

## 2. 스피어만 상관분석(비선형적 상관관계)
- 측정된 두 변수들이 서열척도일 때 사용하는 상관계수다. 스피어만 상관계수는 비모수적 방법으로 관측값의 순위에 대하여 상관계수를 계산하는 방법이다.

```
> X <- c(1, 2, 3, 4, 5)        
> Y <- c(3, 6, 4, 9, 8)        
> cor(X, Y, method = 'spearman')
[1] 0.8
```

# 3. 상관분석 실습
- 10명의 학생들에 대한 학습 시간과 시험 점수에 대한 데이터가 주어졌다. 학습 시간과 시험 점수 사이에 상관관계가 존재하는지 알아보자.

```
> time <- c(8, 6, 7, 3, 2, 4, 2, 7, 2, 3)
> score <- c(33, 22, 18, 6, 23, 10, 9, 30, 11, 13)
> cor.test(time, score)

        Pearson's product-moment correlation

data:  time and score
t = 3.0733, df = 8, p-value = 0.01527
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 0.1978427 0.9331309
sample estimates:
      cor
0.7358112
```

- p-value 값 0.01527이 유의수준 0.05보다 작으므로 귀무가설을 기각한다.
- 두 변수의 상관계수 추정치(cor)는 0.7358112다.
- 두 변수 간(time, score) 상관관계가 있다고 통계적으로 말할 수 있다.