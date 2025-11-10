from st_utils import agent_loader, youtube_loader

agent = agent_loader()
youtube = youtube_loader()

youtube.ui(agent)
