#
import logging
from mimesis.actions.actions import Action
from mimesis.agent.agent import Agent
from mimesis.tools import scrape_text

class Read(Action):
    name = "Read"
    description = "General read action"
    definition = """You can read. When you read, you generate thoughts. Thoughts are brief sentences that relate your personality traits with the text that you are reading. You should always write thoughts in the following format: Thought: "thought". These are examples of thoughts:
* Thought: I find black holes very interesting, but I don't know much about them, I should read more.
* Thought: I wonder how people feel when dying, and if I could experience something similar.
"""

class Analyse(Action):
    name = "Analyse"
    description = "General analyse action"
    definition = """You can analyse. When you analyse, you generate ideas. You should always write ideas in the following format: Idea: idea. These are examples of ideas:
* Idea: I think this book is essential for the understanding of the human mind.
* Idea: The relation between unemployment and the real-state market is very complex.
"""
    url: str = ""

    def memory(self, agent: Agent) -> str:
        return f"I analyzed the following article: {self.url}"


    def do(self, agent: Agent) ->  str:
        logging.warning(f"Analysing website: {self.url}")
        article: str = scrape_text(self.url)
        return f"""{self.definition}

Analyse the following article, delimited by triple equal signs.
===
{article}
===
"""

class FinancialHeadlineAnalysis(Analyse):
    company: str
    period: str
    headline: str

    def memory(self, agent: Agent) -> str:
        return f"I analyzed the following article headline: {self.url}"

    def do(self, agent: Agent) ->  str:
        return f"""
Analyse the headline of the following news article. The analysis must finish with a one-word assessment summarizing how could the information of the headline affect the stock price of the company {self.company}. If you consider the headline is not relevant for the stock price of {self.company}, then say IRRELEVANT. If, on the other hand, the article is relevant for the stock price of {self.company} in the {self.period}, then indicate if the headline is GOOD, BAD, or NEUTRAL. If it is GOOD, you expect the stock of {self.company} to go up {self.period}. If it is BAD, you expect the stock of {self.company} to go down {self.period}. If it is NEUTRAL, then you expect the stock price of {self.company} to remain constant.

Here is an example of an analysis:

Headline: Pro Picks: Missed the boat on Nvidia? Check out these 5 stealth AI plays
Idea: While the headline does not directly criticize Nvidia's performance or business model, its suggestion to look elsewhere for investment opportunities in the AI field can be interpreted as a subtle hint of overvaluation for Nvidia. This could potentially generate short-term selling pressure on the stock.
Assessment: BAD

Headline: {self.headline}
"""

class FinancialArticleAnalysis(Analyse):
    company: str
    period: str
    headline: str

    def memory(self, agent: Agent) -> str:
        return f"I analyzed the following article: {self.url}"

    def do(self, agent: Agent) ->  str:
        return f"""
Analyse the following news article. The analysis must be brief, one paragraph, and finish with a one-word assessment summarizing how could the information provided in the article affect the stock price of the company {self.company}. If you consider the article is not relevant for the stock price of {self.company}, then say IRRELEVANT. If, on the other hand, the article is relevant for the stock price of {self.company} in the {self.period}, then indicate if the headline is GOOD, BAD, or NEUTRAL. If it is GOOD, you expect the stock of {self.company} to go up {self.period}. If it is BAD, you expect the stock of {self.company} to go down {self.period}. If it is NEUTRAL, then you expect the stock price of {self.company} to remain constant.

Here is an example of analysis:
Analysis: The article indicates a positive outlook for the overall market with the Nasdaq index surging and a sixth-straight week of gains, plus the Federal Reserve likely to hold off on a rate hike. However, specific to Nvidia, the sentiment is more negative. Nvidia's stock slid 1.1% for the second consecutive day, even though it recently entered the trillion-dollar valuation club. Some investment professionals are questioning the rapid ascent of Nvidia's valuation and its ability to generate profit commensurate with its market cap, suggesting skepticism about the sustainability of the company's current stock price. While macroeconomic factors can have an influence, the specific concerns around Nvidia's profitability and high growth may exert more pressure on the stock.
Assessment: BAD

Article: {self.headline}
"""

class ReadWebsite(Read):

    #session.headers.update({"User-Agent": CFG.user_agent})
    name: str = "Website reader"
    description: str = "Website reader"
    url: str
    website: str | None = None
    title: str | None = None

    def memory(self, agent: Agent) -> str:
        if self.website == "theguardian":
            return f"I read the following article from The Guardian: {self.title}"
        else:
            return f"I read the following article: {self.url}"

    def do(self, agent: Agent) ->  str:
        logging.warning(f"Reading website: {self.url}")
        article: str = scrape_text(self.url)
        return f"""{self.definition}

Read the following article, delimited by triple equal signs. After reading the article, provide an enumerated list of 5 thoughts:
===
{article}
===
"""