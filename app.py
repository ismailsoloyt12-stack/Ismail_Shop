from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os
import secrets
from pathlib import Path
import mimetypes

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple user storage (in production, use a proper database)
users_db = {}
if os.path.exists('users.json'):
    with open('users.json', 'r') as f:
        users_db = json.load(f)

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    if user_id in users_db:
        user_data = users_db[user_id]
        return User(user_id, user_data['username'], user_data['email'])
    return None

def load_apps():
    """Load apps from the JSON file"""
    if os.path.exists('apps_data.json'):
        with open('apps_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_apps(apps):
    """Save apps to the JSON file"""
    with open('apps_data.json', 'w', encoding='utf-8') as f:
        json.dump(apps, f, indent=2, ensure_ascii=False)

def get_categories():
    """Get unique categories from all apps"""
    apps = load_apps()
    categories = set()
    for app in apps:
        if 'category' in app:
            categories.add(app['category'])
    return sorted(list(categories))

@app.route('/')
def index():
    apps = load_apps()
    categories = get_categories()
    
    # Filter apps by different criteria
    featured_apps = [app for app in apps if app.get('featured', False)][:6]
    trending_apps = sorted(apps, key=lambda x: x.get('downloads', 0), reverse=True)[:6]
    recent_apps = sorted(apps, key=lambda x: x.get('added_date', ''), reverse=True)[:6]
    
    return render_template('index.html', 
                         featured_apps=featured_apps,
                         trending_apps=trending_apps,
                         recent_apps=recent_apps,
                         categories=categories)

@app.route('/app/<app_id>')
def app_detail(app_id):
    apps = load_apps()
    app_data = next((app for app in apps if app['id'] == app_id), None)
    
    if not app_data:
        return "App not found", 404
    
    # Increment view counter
    app_data['views'] = app_data.get('views', 0) + 1
    save_apps(apps)
    
    # Get similar apps (same category)
    similar_apps = [app for app in apps if app.get('category') == app_data.get('category') and app['id'] != app_id][:4]
    
    return render_template('app_detail.html', app=app_data, similar_apps=similar_apps)

@app.route('/category/<category_name>')
def category(category_name):
    apps = load_apps()
    category_apps = [app for app in apps if app.get('category', '').lower() == category_name.lower()]
    
    return render_template('category.html', 
                         category=category_name,
                         apps=category_apps,
                         categories=get_categories())

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    apps = load_apps()
    
    if query:
        results = []
        for app in apps:
            if (query in app.get('name', '').lower() or 
                query in app.get('developer', '').lower() or
                query in app.get('description', '').lower() or
                query in app.get('category', '').lower()):
                results.append(app)
    else:
        results = apps
    
    return render_template('search.html', 
                         query=query,
                         results=results,
                         categories=get_categories())

@app.route('/api/download/<app_id>', methods=['POST'])
def download_app(app_id):
    apps = load_apps()
    app_data = next((app for app in apps if app['id'] == app_id), None)
    
    if not app_data:
        return jsonify({'error': 'App not found'}), 404
    
    # Increment download counter
    app_data['downloads'] = app_data.get('downloads', 0) + 1
    save_apps(apps)
    
    # Check if app has a real file
    has_file = bool(app_data.get('app_file'))
    
    return jsonify({
        'success': True,
        'downloads': app_data['downloads'],
        'message': 'Download started!',
        'has_file': has_file,
        'file_url': f'/download/{app_id}' if has_file else None
    })

@app.route('/download/<app_id>')
def download_file(app_id):
    """Serve actual file download"""
    apps = load_apps()
    app_data = next((app for app in apps if app['id'] == app_id), None)
    
    if not app_data:
        abort(404, description="App not found")
    
    # Get the file name
    app_file = app_data.get('app_file')
    if not app_file:
        abort(404, description="No file available for this app")
    
    # Construct file path
    file_path = Path('Apps_Link') / app_file
    
    # Check if file exists
    if not file_path.exists():
        # Try with app_file_path if available
        if 'app_file_path' in app_data:
            file_path = Path(app_data['app_file_path'])
            if not file_path.exists():
                abort(404, description="File not found on server")
        else:
            abort(404, description="File not found on server")
    
    # Get file MIME type
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if not mime_type:
        mime_type = 'application/octet-stream'
    
    try:
        # Send file with appropriate headers
        return send_file(
            file_path,
            mimetype=mime_type,
            as_attachment=True,
            download_name=app_file
        )
    except Exception as e:
        abort(500, description=f"Error downloading file: {str(e)}")

@app.route('/api/review/<app_id>', methods=['POST'])
@login_required
def add_review(app_id):
    apps = load_apps()
    app_data = next((app for app in apps if app['id'] == app_id), None)
    
    if not app_data:
        return jsonify({'error': 'App not found'}), 404
    
    data = request.json
    review = {
        'user': current_user.username,
        'rating': data.get('rating', 5),
        'comment': data.get('comment', ''),
        'date': datetime.now().isoformat()
    }
    
    if 'reviews' not in app_data:
        app_data['reviews'] = []
    
    app_data['reviews'].append(review)
    
    # Update average rating
    ratings = [r['rating'] for r in app_data['reviews']]
    app_data['rating'] = sum(ratings) / len(ratings)
    app_data['review_count'] = len(app_data['reviews'])
    
    save_apps(apps)
    
    return jsonify({'success': True, 'review': review})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user by username
        user_data = None
        user_id = None
        for uid, udata in users_db.items():
            if udata['username'] == username:
                user_data = udata
                user_id = uid
                break
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_id, user_data['username'], user_data['email'])
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if username already exists
        for uid, udata in users_db.items():
            if udata['username'] == username:
                flash('Username already exists', 'error')
                return render_template('register.html')
        
        # Create new user
        user_id = str(len(users_db) + 1)
        users_db[user_id] = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'created_at': datetime.now().isoformat()
        }
        
        # Save users database
        with open('users.json', 'w') as f:
            json.dump(users_db, f, indent=2)
        
        # Log in the new user
        user = User(user_id, username, email)
        login_user(user)
        
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/firebase-auth', methods=['POST'])
def firebase_auth():
    """Sync Firebase authentication with Flask backend"""
    data = request.json
    
    if not data or not data.get('uid'):
        return jsonify({'error': 'Invalid authentication data'}), 400
    
    firebase_uid = data['uid']
    email = data.get('email', '')
    display_name = data.get('displayName', '')
    photo_url = data.get('photoURL', '')
    
    # Use Firebase UID as user ID with 'firebase_' prefix
    user_id = f"firebase_{firebase_uid}"
    
    # Check if user exists
    if user_id not in users_db:
        # Create new user from Firebase data
        username = display_name if display_name else email.split('@')[0]
        
        # Ensure unique username
        base_username = username
        counter = 1
        while any(u['username'] == username for u in users_db.values()):
            username = f"{base_username}{counter}"
            counter += 1
        
        users_db[user_id] = {
            'username': username,
            'email': email,
            'password': generate_password_hash(secrets.token_hex(32)),  # Random password for Firebase users
            'firebase_uid': firebase_uid,
            'display_name': display_name,
            'photo_url': photo_url,
            'created_at': datetime.now().isoformat(),
            'auth_provider': 'firebase',
            'favorites': []
        }
        
        # Save users database
        with open('users.json', 'w') as f:
            json.dump(users_db, f, indent=2)
    else:
        # Update existing user info
        users_db[user_id]['display_name'] = display_name
        users_db[user_id]['photo_url'] = photo_url
        users_db[user_id]['last_login'] = datetime.now().isoformat()
        
        with open('users.json', 'w') as f:
            json.dump(users_db, f, indent=2)
    
    # Create Flask user session
    user = User(user_id, users_db[user_id]['username'], email)
    login_user(user, remember=True)
    
    return jsonify({
        'success': True,
        'username': users_db[user_id]['username'],
        'message': 'Authentication synced successfully'
    })

@app.route('/api/firebase-logout', methods=['POST'])
def firebase_logout():
    """Handle Firebase logout and clear Flask session"""
    logout_user()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/favorite/<app_id>', methods=['POST'])
@login_required
def toggle_favorite(app_id):
    # Load user favorites
    if not hasattr(current_user, 'favorites'):
        current_user.favorites = []
    
    if app_id in current_user.favorites:
        current_user.favorites.remove(app_id)
        favorited = False
    else:
        current_user.favorites.append(app_id)
        favorited = True
    
    # Save to user data
    if current_user.id in users_db:
        users_db[current_user.id]['favorites'] = current_user.favorites
        with open('users.json', 'w') as f:
            json.dump(users_db, f, indent=2)
    
    return jsonify({'favorited': favorited})

@app.route('/favorites')
@login_required
def favorites():
    apps = load_apps()
    user_favorites = users_db.get(current_user.id, {}).get('favorites', [])
    favorite_apps = [app for app in apps if app['id'] in user_favorites]
    
    return render_template('favorites.html', apps=favorite_apps)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
