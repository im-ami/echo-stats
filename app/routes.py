from flask import Blueprint, redirect, session, url_for, request, render_template
from app.auth import sp_oauth, get_spotify

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    if get_spotify():
        return redirect(url_for('main_routes.get_playlists'))
    return render_template('welcome.html')

@main_routes.route('/login')  # Changed from '/' to '/login'
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@main_routes.route('/callback')
def callback():
    if 'code' not in request.args:
        return redirect(url_for('main_routes.home'))
        
    try:
        token_info = sp_oauth.get_access_token(request.args['code'], check_cache=False)
        
        if token_info:
            # Store token info in session
            session['token_info'] = token_info
            return redirect(url_for('main_routes.dashboard'))
    except Exception as e:
        print(f"Error in callback: {str(e)}")
        session.clear()
        
    return redirect(url_for('main_routes.home'))

@main_routes.route('/playlists')
def get_playlists():
    sp = get_spotify()
    if not sp:
        return redirect(url_for('main_routes.home'))
    
    playlists = sp.current_user_playlists()
    return render_template('playlists.html', playlists=playlists['items'])

@main_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main_routes.home'))

@main_routes.route('/dashboard')
def dashboard():
    sp = get_spotify()
    if not sp:
        return redirect(url_for('main_routes.home'))
    
    # Fetch top artists
    top_artists = sp.current_user_top_artists(limit=5, time_range='medium_term')
    
    # Fetch top tracks
    top_tracks = sp.current_user_top_tracks(limit=5, time_range='medium_term')
    
    # Fetch recently played to analyze activity by hour
    recently_played = sp.current_user_recently_played(limit=50)
    
    # Process activity by hour
    activity_by_hour = [0] * 24
    for item in recently_played['items']:
        hour = int(item['played_at'][11:13])  # Extract hour from timestamp
        activity_by_hour[hour] += 1
    
    # Process top genres from top artists
    genres = {}
    for artist in top_artists['items']:
        for genre in artist['genres']:
            genres[genre] = genres.get(genre, 0) + 1
    
    # Sort genres by count and get top 5
    top_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:5]
    genre_names = [genre[0] for genre in top_genres]
    genre_counts = [genre[1] for genre in top_genres]
    
    # Get top albums from top tracks
    albums = {}
    for track in top_tracks['items']:
        album = track['album']
        album_key = f"{album['name']} - {album['artists'][0]['name']}"
        albums[album_key] = albums.get(album_key, 0) + 1
    
    top_albums = [
        {'name': name.split(' - ')[0], 'artist': name.split(' - ')[1]} 
        for name in sorted(albums, key=albums.get, reverse=True)[:5]
    ]

    return render_template('dashboard.html',
                         top_artists=top_artists['items'],
                         top_tracks=top_tracks['items'],
                         top_albums=top_albums,
                         activity_hours=list(range(24)),
                         activity_counts=activity_by_hour,
                         genre_names=genre_names,
                         genre_counts=genre_counts)