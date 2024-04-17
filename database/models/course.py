from enum import Enum
from sqlmodel import SQLModel, Field


class Movie(SQLModel):
    class Genre(str, Enum):
        action = "Action"
        adventure = "Adventure"
        animation = "Animation"
        biography = "Biography"
        comedy = "Comedy"
        crime = "Crime"
        documentary = "Documentary"
        drama = "Drama"
        family = "Family"
        fantasy = "Fantasy"
        film_noir = "Film-Noir"
        history = "History"
        horror = "Horror"
        music = "Music"
        musical = "Musical"
        mystery = "Mystery"
        romance = "Romance"
        science_fiction = "Science-Fiction"
        sport = "Sport"
        superhero = "Superhero"
        thriller = "Thriller"
        war = "War"
        western = "Western"

    class Rating(str, Enum):
        g = "G"
        pg = "PG"
        pg_13 = "PG-13"
        r = "R"
        nc_17 = "NC-17"


class Hero(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        allow_mutation=False,
    )
    name: str = Field(
        index=True,
        nullable=False,
        max_length=50,
        unique=True,
        allow_mutation=True,
        title="Hero Name",
    )
    secret_name: str
    age: int | None = None
