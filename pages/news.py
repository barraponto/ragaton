from st_utils import agent_loader, news_loader

agent = agent_loader()
news = news_loader()

news.ui(agent)
