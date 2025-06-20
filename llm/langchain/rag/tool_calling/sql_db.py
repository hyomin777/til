import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from env import OPENAI_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

import sqlite3
import requests
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent


def create_chinook_database():
    """Chinook 데이터베이스를 메모리에 생성하고 SQLAlchemy 엔진을 반환합니다."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)

    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

# 데이터베이스 엔진 생성
db_engine = create_chinook_database()

# SQLDatabase 객체 생성
db = SQLDatabase(db_engine)

# OpenAI의 GPT-4o-mini 모델 초기화
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# SQLDatabaseToolkit 객체 생성
toolkit = SQLDatabaseToolkit(db=db, llm=llm)



# 프롬프트 템플릿 가져오기
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

# 시스템 메시지 생성
system_message = prompt_template.format(dialect="SQLite", top_k=5)

# ReAct 에이전트 생성
agent_executor = create_react_agent(
    llm, 
    toolkit.get_tools(), 
    prompt=system_message
)



# 예제 쿼리 정의
example_query = "2009년에 가장 많이 팔린 장르는 무엇이며, 해당 장르의 총 매출액은 얼마인가요?"

# 에이전트를 사용하여 쿼리 실행
events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)

# 결과 출력
for event in events:
    event["messages"][-1].pretty_print()