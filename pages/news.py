from st_utils import agent_loader, news_loader

agent = agent_loader()
news = news_loader()

"""
# Ragaton loves reading the news!
"""

news.ui(agent)
