head <- head(iris, 3)
summary <- summary(iris)
str(iris)

copy_iris <- iris
copy_iris[sample(1:150, 30), 1] <- NA

# 결측치 시각화화
install.packages('Amelia')
library(Amelia)
missmap(copy_iris)

print(dim(copy_iris))
# 단순 대치법
copy_iris <- copy_iris[complete.cases(copy_iris),]
print(dim(copy_iris))

copy_iris <- iris
copy_iris[sample(1:150, 30), 1] <- NA

# 평균 대치법
meanValue <- mean(copy_iris$Sepal.Length, na.rm=T) # 결측값을 제외한 평균 계산
copy_iris$Sepal.Length[is.na(copy_iris$Sepal.Length)] <- meanValue # 평균 대치

# 중앙값 대치
install.packages('DMwR2')
library(DMwR2)
copy_iris <- iris
copy_iris[sample(1:150, 30), 1] <- NA
copy_iris <- centralImputation(copy_iris)

# 단순 확률 대치법
copy_iris <- iris
copy_iris[sample(1:150, 30), 1] <- NA
copy_iris <- knnImputation(copy_iris, k = 10)

# 다중 대치법
copy_iris <- iris
copy_iris[sample(1:150, 30), 1] <- NA
library(Amelia)
iris_imp <- amelia(copy_iris, m=3, cs="Species")
# cs는 cross-sectional로 분석에 포함될 정보를 의미
# 위 amelia에서 m 값을 그대로 imputation의 데이터셋에 사용한다.
copy_iris$Sepal.Length <- iris_imp$imputations[[3]]$Sepal.Length