#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import array, string
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Venue, Artist, Show
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db = SQLAlchemy(app)
db.init_app(app)
# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues/')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  cities = db.session.query(Venue.city,Venue.state).all()
  venues = Venue.query.all()

  data = list(set(cities))

  return render_template('pages/venues.html', areas=data, venues=venues)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term')
  
  venues = Venue.query.filter(Venue.name.ilike("%"+search_term+"%")).all()

  count = len(venues)


  return render_template('pages/search_venues.html', results=venues,count=count, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data=Venue.query.get(venue_id)

  # shows = Show.query.filter_by(venue_id=venue_id).all()
  shows = db.session.query(Show).join(Venue, Show.venue_id == venue_id)

  upcoming_shows = [] 
  past_shows = []
  for show in shows:
    if show.start_time >= datetime.now():
      upcoming_shows.append(show)
    else:
      past_shows.append(show)


  return render_template('pages/show_venue.html', venue=data,upcoming_shows=upcoming_shows,past_shows=past_shows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    error = False
    form = VenueForm(request.form)
    try:
        name = form.name.data
        city = form.city.data
        state = form.state.data
        address = form.address.data
        phone = form.phone.data
        genres = request.form.getlist('genres')
        image_link = form.image_link.data
        facebook_link = form.facebook_link.data
        website = form.website.data
        seeking_talent = form.seeking_talent.data
        seeking_description = form.seeking_description.data
       
        venue = Venue(name = name, city=city, 
                state=state, address=address,phone=phone,
                website=website,genres=genres,image_link=image_link,
                facebook_link=facebook_link,seeking_talent=seeking_talent,
                seeking_description=seeking_description )

        db.session.add(venue)
        db.session.commit()

        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    except:
        error = True
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
    finally:
        db.session.close()
    if not error:
        return render_template('pages/home.html')

 
     # TODO: on unsuccessful db insert, flash an error instead.
     # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
     # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage


    venueId = request.form.get("delete_venue")
    venue = Venue.query.filter_by(id=venueId).first()
    db.session.delete(venue)
    db.session.commit()
    return redirect("/")


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.

   
  search_term = request.form.get('search_term')
  
  artist = Artist.query.filter(Artist.name.ilike("%"+search_term+"%")).all()

  count = len(artist)

  return render_template('pages/search_artists.html',count=count, results=artist, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
 
  data=Artist.query.get(artist_id)
  shows = db.session.query(Show).join(Artist, Show.artist_id == artist_id)
  upcoming_shows = [] 
  past_shows = []
  for show in shows:
    if show.start_time >= datetime.now():
      upcoming_shows.append(show)
    else:
      past_shows.append(show)

  return render_template('pages/show_artist.html', artist=data, upcoming_shows=upcoming_shows, past_shows=past_shows)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()


  artist = Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  form = ArtistForm(request.form)
  try:
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        genres = request.form.getlist("genres")
        image_link = form.image_link.data
        facebook_link = form.facebook_link.data
        website = form.website.data
        seeking_venue = form.seeking_venue.data
        seeking_description = form.seeking_description.data
       
        editArtist = Artist.query.get(artist_id)
        editArtist.name = name
        editArtist.city = city
        editArtist.state = state
        editArtist.phone = phone
        editArtist.genres = genres
        editArtist.image_link = image_link
        editArtist.facebook_link = facebook_link
        editArtist.website = website
        editArtist.seeking_venue= seeking_venue
        editArtist.seeking_description = seeking_description
        
        db.session.commit()
       

       # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully edited!')

  except:
      error = True
      db.session.rollback()
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Artist could not be edited.')
  finally:
      db.session.close()
  if not error:
      return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes


    error = False
    form = VenueForm(request.form)


    try:
        name = form.name.data
        city = form.city.data
        state = form.state.data
        address = form.address.data
        phone = form.phone.data
        genres = request.form.getlist("genres")
        image_link = form.image_link.data
        facebook_link = form.facebook_link.data
        website = form.website.data
        seeking_talent = form.seeking_talent.data
        seeking_description = form.seeking_description.data
        
        editVenue = Venue.query.get(venue_id)
        editVenue.name = name
        editVenue.city = city
        editVenue.state = state
        editVenue.address = address
        editVenue.phone = phone
        editVenue.genres = genres
        editVenue.image_link = image_link
        editVenue.facebook_link = facebook_link
        editVenue.website = website
        editVenue.seeking_talent = seeking_talent
        editVenue.seeking_description = seeking_description

        db.session.commit()

        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully Edited!')

    except:
        error = True
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue could not be edited.')
    finally:
        db.session.close()
    if not error:
      return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion


  error = False
  form = ArtistForm(request.form)
  try:
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        genres = request.form.getlist("genres")
        image_link = form.image_link.data
        facebook_link = form.facebook_link.data
        website = form.website.data
        seeking_venue= form.seeking_venue.data
        seeking_description = form.seeking_description.data
       
        artist = Artist(name = name, city=city, state=state,
                 phone=phone,genres=genres,image_link=image_link,
                 facebook_link=facebook_link, website=website, 
                 seeking_venue=seeking_venue,seeking_description=seeking_description)
        db.session.add(artist)
        db.session.commit()

       # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
      error = True
      db.session.rollback()
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
  finally:
      db.session.close()
  if not error:
      return render_template('pages/home.html')




#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = list(Show.query.all())
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

   error = False
   form = ShowForm(request.form)
   try:
       artist_id = form.artist_id.data
       venue_id = form.venue_id.data
       start_time = form.start_time.data
       
      #  venue = Venue.query.get(venue_id)
      #  artist = Artist.query.get(artist_id)
       
       show = Show(venue_id=venue_id,artist_id=artist_id,start_time=start_time)
      #  venue.shows.append(show)
      #  artist.shows.append(show)    

       db.session.add(show)
       db.session.commit()      

       # on successful db insert, flash success
       flash('Show was successfully listed!')
 
   except:
       error = True
       db.session.rollback()
       # TODO: on unsuccessful db insert, flash an error instead.
       flash('An error occurred. Show could not be listed.')
   finally:
       db.session.close()
   if not error:
       # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
       return render_template('pages/home.html')
 
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
