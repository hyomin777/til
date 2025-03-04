data <- data.frame(
    student_number = c(1, 2, 1, 2),
    semester = c(1, 1, 2, 2),
    math_score = c(60, 90, 70, 90),
    eng_score = c(80, 70, 40, 60)
)

install.packages("reshape")
library(reshape)
melted_data <- melt(data, id = c("student_number", "semester"))

casted_data1 <- cast(melted_data, student_number ~ variable, mean)
casted_data2 <- cast(melted_data, student_number ~ semester, mean)
casted_data3 <- cast(melted_data, student_number ~ variable, max)

install.packages("sqldf")
library(sqldf)
sql_df1 <- sqldf("select * from data")
sql_df2 <- sqldf("select * from data where student_number = 1")
sql_df3 <- sqldf("select math_score, eng_score from data group by student_number")
sql_df4 <- sqldf("select avg(math_score), avg(eng_score) from data group by student_number")

install.packages("plyr")
library(plyr)

data <- data.frame(class = c("A", "A", "B", "B"), math = c(50, 70, 60, 90), english = c(70, 80, 60, 80))

ddply_df1 <- ddply(data, "class", summarise, math_avg = mean(math), eng_avg = mean(english))
ddply_df2 <- ddply(data, "class", transform, math_avg = mean(math), eng_avg = mean(english))

data <- data.frame(
    year = c(2012, 2012, 2012, 2012, 2013, 2013, 2013, 2013),
    month = c(1, 1, 2, 2, 1, 1, 2, 2),
    value = c(3, 5, 7, 9, 1, 5, 4, 6)
)

ddply_df3 <- ddply(data, c("year", "month"), summarise, value_avg = mean(value))
ddply_df4 <- ddply(
    data,
    c("year", "month"),
    function(x) {
        value_avg <- mean(x$value) # 평균 계산
        value_sd <- sd(x$value) # 표준편차 계산
        data.frame(avg = value_avg, sd = value_sd, avg_sd = value_avg / value_sd) # 데이터 프레임으로 반환
    }
)


install.packages("data.table")
library(data.table)
# 같은 데이터로 4800만 개의 행을 갖는 데이터 프레임과 데이터 테이블을 생성
year <- rep(c(2012:2015), each = 12000000)
month <- rep(rep(c(1:12), each = 1000000), 4)
value <- runif(48000000)

DataFrame <- data.frame(year, month, value)
DataTable <- as.data.table(DataFrame)

# 검색 시간을 측정
frame_time <- system.time(DataFrame[DataFrame$year == 2012, ])
table_time <- system.time(DataTable[DataTable$year == 2012, ])

# 데이터 테이블의 year 컬럼에 키 값을 설정
# 컬럼이 키 값으로 설정될 경우 자동 오름차순 정렬
setkey(DataTable, year)
# 키 값으로 설정된 컬럼과 J 표현식을 사용한 검색 시간 측정정
table_key_time <- system.time(DataTable[J(2012)])
