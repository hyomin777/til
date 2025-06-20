import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__))))))
from env import OPENAI_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

from langchain_experimental.tools import PythonAstREPLTool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

python_repl = PythonAstREPLTool()

llm = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0,
    max_tokens=500,
)

agent = initialize_agent(
    [python_repl],
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = agent.invoke(
'''
1부터 10까지의 숫자 중 짝수만 출력하는 Python 코드를 작성하고 실행해주세요.
그리고 그 결과를 설명해주세요.
'''
)
print(result)