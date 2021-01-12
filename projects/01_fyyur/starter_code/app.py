#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import datetime
import json
import dateutil.parser
import babel
from flask import (
  Flask,
  render_template,
  request,
  Response,
  flash,
  redirect,
  url_for
)
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Artist, Venue, Show
from sqlalchemy import or_
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
  # ensure value is parsed correctly in case it is already a datetime object
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  """Show a list of existing venues."""
  venues = Venue.query.all()
  cities = Venue.query.distinct('city', 'state').all()

  data = []
  for city in cities:
    data.append({
      "city": city.city,
      "state": city.state,
      "venues": [
        {
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(
            [show for show in venue.shows if show.start_time > datetime.now()]
          )
        }
        for venue in venues if venue.city == city.city \
          and venue.state == city.state
      ]
    })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  """Search for a venue."""
  search_term = "%{}%".format(request.form["search_term"])
  venues = Venue.query.filter(Venue.name.ilike(search_term)).all()
  response = {
    "count": len(venues),
    "data": [
      {
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len([show for show in venue.shows if \
        show.start_time > datetime.now()])
      }
      for venue in venues
    ]
  }
  return render_template(
    'pages/search_venues.html',
    results=response,
    search_term=request.form.get('search_term', '')
  )

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  """Show the details for a specific venue."""
  venue = Venue.query.get(venue_id)
  past_shows = Show.query.join(Venue).join(Artist).filter(
    Show.venue_id == venue_id,
    Show.artist_id == Artist.id,
    Show.start_time < datetime.now(),
  ).all()
  upcoming_shows = Show.query.join(Venue).join(Artist).filter(
    Show.venue_id == venue_id,
    Show.artist_id == Artist.id,
    Show.start_time > datetime.now(),
  ).all()
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres if venue.genres else [],
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [
      {
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      }
      for show in past_shows
    ],
    "upcoming_shows": [
      {
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time
      }
      for show in upcoming_shows
    ],
    "past_shows_count": len(
      [show for show in venue.shows if show.start_time < datetime.now()]
    ),
    "upcoming_shows_count": len(
      [show for show in venue.shows if show.start_time > datetime.now()]
    ),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  """Create a new venue on Fyur."""
  error = False
  form = VenueForm(request.form)
  try:
    new_venue = Venue()
    form.populate_obj(new_venue)
    db.session.add(new_venue)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()

  if error:
    flash(
      'An error occurred. Venue ' + form["name"].data + ' could not be listed.'
    )
  else:
    flash('Venue ' + form["name"].data + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>', methods=['POST'])
def delete_venue(venue_id):
  """Delete a venue from Fyur."""
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()

  if error:
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
  else:
    flash('Venue ' + venue.name + ' was successfully deleted!')
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  """Show all artists on Fyur."""
  artists = Artist.query.all()
  data=[
    {
      "id": artist.id,
      "name": artist.name,
    }
    for artist in artists
  ]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  """Search for an artist."""
  search_term = "%{}%".format(request.form["search_term"])
  artists = Artist.query.filter(Artist.name.ilike(search_term)).all()
  response = {
    "count": len(artists),
    "data": [
      {
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": len([show for show in artist.shows \
           if show.start_time > datetime.now()])
      }
      for artist in artists
    ]
  }
  return render_template(
    'pages/search_artists.html',
    results=response,
    search_term=request.form.get('search_term', '')
  )

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  """Show details for a specific artist"""
  artist = Artist.query.get(artist_id)
  past_shows = Show.query.join(Artist).join(Venue).filter(
    Show.artist_id == artist_id,
    Show.venue_id == Venue.id,
    Show.start_time < datetime.now(),
  ).all()
  upcoming_shows = Show.query.join(Artist).join(Venue).filter(
    Show.artist_id == artist_id,
    Show.venue_id == Venue.id,
    Show.start_time > datetime.now(),
  ).all()

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [
      {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time
      }
      for show in past_shows
    ],
    "upcoming_shows": [
      {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time
      }
      for show in upcoming_shows
    ],
    "past_shows_count": len([show for show in artist.shows \
      if show.start_time < datetime.now()]),
    "upcoming_shows_count": len([show for show in artist.shows \
      if show.start_time > datetime.now()]),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(
    name=artist.name,
    genres=artist.genres,
    city=artist.city,
    state=artist.state,
    phone=artist.phone,
    website=artist.website,
    facebook_link=artist.facebook_link,
    seeking_venue=artist.seeking_venue,
    seeking_description=artist.seeking_description,
    image_link=artist.image_link,
  )
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  """Edit details for an existing artist."""
  error = False
  form = ArtistForm(request.form)
  artist = Artist.query.get(artist_id)
  try:
    form.populate_obj(artist)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()

  if error:
    flash(
      'An error occurred. Artist ' + form["name"].data + ' could not be updated.'
    )
  else:
    flash(
      'Information for artist ' + form["name"].data + ' was successfully updated!'
    )

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(
    name=venue.name,
    genres=venue.genres,
    city=venue.city,
    state=venue.state,
    address=venue.address,
    phone=venue.phone,
    website=venue.website,
    facebook_link=venue.facebook_link,
    seeking_talent=venue.seeking_talent,
    seeking_description=venue.seeking_description,
    image_link=venue.image_link,
  )
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  """Edit details for an existing venue."""
  error = False
  form = VenueForm(request.form)
  venue = Venue.query.get(venue_id)
  try:
    form.populate_obj(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()

  if error:
    flash(
      'An error occurred. Venue ' + form["name"].data + ' could not be updated.'
    )
  else:
    flash(
      'Information for venue ' + form["name"].data + ' was successfully updated!'
    )

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  """Add a new artist."""
  error = False
  form = ArtistForm(request.form)
  try:
    new_artist = Artist()
    form.populate_obj(new_artist)
    db.session.add(new_artist)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()

  if error:
    flash(
      'An error occurred. Artist ' + form["name"].data + ' could not be listed.'
    )
  else:
    flash('Artist ' + form["name"].data + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  """List past and upcoming shows."""
  shows = Show.query.all()
  data = [
    {
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist.name,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time": show.start_time,
    }
    for show in shows
  ]

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  """Add a new show for a specific venue and artist."""
  error = False
  form = ShowForm(request.form)
  try:
    new_show = Show()
    form.populate_obj(new_show)
    db.session.add(new_show)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  
  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')
  return render_template('pages/home.html')


@app.route('/shows/search', methods=['POST'])
def search_shows():
  """Search past and upcoming shows by artist or venue name."""
  search_term = "%{}%".format(request.form["search_term"])
  shows = Show.query.join(Artist).join(Venue).filter(
    or_(
      Artist.name.ilike(search_term),
      Venue.name.ilike(search_term),
    )).all()

  response = {
    "count": len(shows),
    "data": [
      {
        "id": show.id,
        "artist_name": show.artist.name,
        "venue_name": show.venue.name,
        "start_time": show.start_time,
      }
      for show in shows
    ]
  }
  return render_template(
    'pages/search_shows.html',
    results=response,
    search_term=request.form.get('search_term', '')
  )


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
      Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
      )
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
