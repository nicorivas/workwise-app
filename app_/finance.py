from mimesis import Agent
from mimesis import FinancialHeadlineAnalysis
import pandas as pd
import duckdb

def load_agent() -> Agent:
    agent = Agent()
    agent.load("../../library/agents/financial_advisor.json")
    return agent

def load_news() -> pd.DataFrame:
    con = duckdb.connect(database='../../library/articles.duckdb')
    news = con.execute("SELECT * FROM articles_newsapi").df()
    return news

agent = load_agent()
news = load_news()

analyseHeadline = FinancialHeadlineAnalysis(company="Nvidia", period="the next day", headline=news.iloc[2]["title"])
print(agent.prompt(definition=False, action=analyseHeadline))
