# 데이터 마이닝을 위한 데이터 분할 시행
# train 데이터는 index 값을 1로 70%, test 데이터는 index 값을 2로 30% 생성
index <- sample(c(1, 2), nrow(iris), replace = TRUE, prob = c(0.7, 0.3))
train <- iris[index == 1, ]
test <- iris[index == 2, ]

install.packages("rpart")
library(rpart)

result <- rpart(data = train, Species ~ .)
plot(result, margin = 0.3)
text(result)

# train 데이터로 구축된 모형을 test 데이터로 검정
pred <- predict(result, newdata = test, type = "class")
# test 데이터의 실제값(condition)과 예측값(pred)으로 표를 작성
table(condition = test$Species, pred)
# 실제 virginica를 versicolor로 잘못 예측한 값이 2개 존재
# 데이터 분할에 따라 다른 결과가 나타난다.

result
# 106개로 구성된 train 데이터셋
# 1번은 뿌리마디로 106개 중 68개의 virginica를 보유하고 있다.
# 2번과 3번은 1번 뿌리마디의 자식마디다.
# 2번은 34개의 setosa 중 0개가 잘못 분류되었음을 의미한다.
# '*' 표시는 자식마디가 없음을 의미, 따라서 2번 노드는 끝마디다.
# 3번은 72개의 vriginica 중 34개가 잘못 분류되었음을 의미한다.
# 6번과 7번은 3번의 자식마디다.
# 6번은 37개의 versicolor 중 4개가 잘못 분류되었음을 의미한다.
# 7번은 35개의 virginica 중 1개가 잘못 분류되었음을 의미한다.
# 괄호 안의 숫자는 (setoca, versicolor, virginica)의 비율을 가리킨다.