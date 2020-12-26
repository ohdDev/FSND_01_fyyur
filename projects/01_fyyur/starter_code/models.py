from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column( db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column( db.Integer, db.ForeignKey('venues.id'),nullable=False)
    start_time = db.Column( db.DateTime(),nullable=False)
    venue = db.relationship("Venue", back_populates="artists")
    artist = db.relationship("Artist", back_populates="venues")


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.String())
    seeking_description = db.Column(db.String(255))
    artists = db.relationship("Show", back_populates="venue",cascade="all, delete")

     



# TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.String(), default=False)
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(255))
    venues = db.relationship("Show", back_populates="artist",cascade="all, delete")
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
