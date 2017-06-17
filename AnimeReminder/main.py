from AnimeDatabase import AnimeDatabase
from EpisodeDatabase import EpisodeDatabase

AnimeDatabase = AnimeDatabase()
EpisodeDatabase = EpisodeDatabase()
animes = AnimeDatabase.getAll()
for anime in animes:
    EpisodeDatabase.update(anime)
