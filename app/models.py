import sqlalchemy
metadata = sqlalchemy.MetaData()
guests = sqlalchemy.Table(
    "guests",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("slug", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("church_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("church_lat", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("church_lng", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("reception_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("reception_lat", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("reception_lng", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("rsvp", sqlalchemy.String, nullable=True),
)
