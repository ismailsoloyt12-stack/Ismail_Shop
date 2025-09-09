from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file, abort, make_response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
import secrets
from pathlib import Path
import mimetypes
import uuid
from functools import wraps
import hashlib
from collections import defaultdict
import time
import sys

# --- 1. الإعدادات الأساسية للتطبيق ---
app = Flask(__name__)
# FIXED: Use absolute path that works on both Windows and Linux
project_path = os.path.dirname(os.path.abspath(__file__))
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Enable CORS for API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# --- 2. الدوال المساعدة (Helper Functions) ---
# تم نقلها هنا عشان تكون مُعرفة قبل استخدامها

def load_apps():
    """Load apps from the JSON file"""
    # FIXED: Use absolute path for cross-platform compatibility
    apps_file = os.path.join(project_path, 'apps_data.json')
    if os.path.exists(apps_file):
        try:
            with open(apps_file, 'r', encoding='utf-8') as f:
                apps = json.load(f)
                return apps
        except json.JSONDecodeError as e:
            # Log error but return empty list to prevent crashes
            return []
    return []

def save_apps(apps):
    """Save apps to the JSON file"""
    # FIXED: Use absolute path for cross-platform compatibility
    apps_file = os.path.join(project_path, 'apps_data.json')
    with open(apps_file, 'w', encoding='utf-8') as f:
        json.dump(apps, f, indent=2, ensure_ascii=False)

def get_categories():
    """Get unique categories from all apps"""
    apps = load_apps()
    categories = set()
    for app_item in apps:
        if 'category' in app_item:
            categories.add(app_item['category'])
    return sorted(list(categories))

def log_activity(user_id, activity_type, description):
    """Log user activity"""
    activity = {
        'id': str(uuid.uuid4()),
        'type': activity_type,
        'description': description,
        'timestamp': datetime.now().isoformat(),
        'time_ago': 'Just now'
    }
    activities_db[user_id].append(activity)
    activities_db[user_id] = activities_db[user_id][-100:] # Keep last 100
    # FIXED: Use absolute path for cross-platform compatibility
    activities_file = os.path.join(project_path, 'activities.json')
    with open(activities_file, 'w') as f:
        json.dump(dict(activities_db), f, indent=2)

def send_notification(user_id, title, message, type='info'):
    """Send notification to user"""
    if user_id in users_db:
        if 'notifications' not in users_db[user_id]:
            users_db[user_id]['notifications'] = []

        notification = {
            'id': str(uuid.uuid4()),
            'title': title,
            'message': message,
            'type': type,
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        users_db[user_id]['notifications'].append(notification)
        users_db[user_id]['notifications'] = users_db[user_id]['notifications'][-50:] # Keep last 50
        # FIXED: Use absolute path for cross-platform compatibility
        users_file = os.path.join(project_path, 'users.json')
        with open(users_file, 'w') as f:
            json.dump(users_db, f, indent=2)

# Admin decorator
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# --- 3. تحميل البيانات من ملفات JSON ---

# FIXED: Use absolute paths for all JSON file loading
users_db = {}
users_file = os.path.join(project_path, 'users.json')
if os.path.exists(users_file):
    with open(users_file, 'r') as f:
        users_db = json.load(f)

collections_db = {}
collections_file = os.path.join(project_path, 'collections.json')
if os.path.exists(collections_file):
    with open(collections_file, 'r') as f:
        collections_db = json.load(f)

activities_db = defaultdict(list)
activities_file = os.path.join(project_path, 'activities.json')
if os.path.exists(activities_file):
    with open(activities_file, 'r') as f:
        activities_db = defaultdict(list, json.load(f))

analytics_db = defaultdict(lambda: defaultdict(int))
analytics_file = os.path.join(project_path, 'analytics.json')
if os.path.exists(analytics_file):
    with open(analytics_file, 'r') as f:
        loaded_data = json.load(f)
        for key, value in loaded_data.items():
            analytics_db[key] = defaultdict(int, value)


# --- 4. تعريف كلاس المستخدم وإعدادات LoginManager ---

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = users_db.get(id, {}).get('is_admin', False)
        self.avatar = users_db.get(id, {}).get('avatar', None)
        self.bio = users_db.get(id, {}).get('bio', '')
        self.favorites = users_db.get(id, {}).get('favorites', [])
        self.wishlist = users_db.get(id, {}).get('wishlist', [])
        self.downloads_history = users_db.get(id, {}).get('downloads_history', [])
        self.followers = users_db.get(id, {}).get('followers', [])
        self.following = users_db.get(id, {}).get('following', [])

@login_manager.user_loader
def load_user(user_id):
    if user_id in users_db:
        user_data = users_db[user_id]
        return User(user_id, user_data['username'], user_data['email'])
    return None


# --- 5. مسارات الموقع (Routes) ---

@app.route('/')
def index():
    apps = load_apps()
    # Exclude Premium Unlocked apps from regular sections
    regular_apps = [app for app in apps if app.get('category') != 'Premium Unlocked']
    categories = get_categories()
    featured_apps = [app for app in regular_apps if app.get('featured', False)][:6]
    trending_apps = sorted(regular_apps, key=lambda x: x.get('downloads', 0), reverse=True)[:6]
    recent_apps = sorted(regular_apps, key=lambda x: x.get('added_date', ''), reverse=True)[:6]
    # Check if there are any premium unlocked apps
    has_premium_apps = any(app.get('category') == 'Premium Unlocked' for app in apps)
    return render_template('index.html',
                         featured_apps=featured_apps,
                         trending_apps=trending_apps,
                         recent_apps=recent_apps,
                         categories=categories,
                         has_premium_apps=has_premium_apps)

@app.route('/app/<app_id>')
def app_detail(app_id):
    apps = load_apps()
    app_data = next((app for app in apps if app['id'] == app_id), None)
    if not app_data:
        abort(404, description="App not found")
    app_data['views'] = app_data.get('views', 0) + 1
    save_apps(apps)
    # For Premium Unlocked apps, only show similar Premium Unlocked apps
    if app_data.get('category', '').lower() == 'premium unlocked':
        similar_apps = [app for app in apps
                       if app.get('category', '').lower() == 'premium unlocked'
                       and app['id'] != app_id][:4]
        # Use special template for Premium Unlocked apps if needed
        return render_template('app_detail_premium.html' if os.path.exists('templates/app_detail_premium.html')
                              else 'app_detail.html',
                              app=app_data, similar_apps=similar_apps)
    else:
        # For regular apps, exclude Premium Unlocked from similar apps
        similar_apps = [app for app in apps
                       if app.get('category') == app_data.get('category')
                       and app['id'] != app_id
                       and app.get('category', '').lower() != 'premium unlocked'][:4]
    return render_template('app_detail.html', app=app_data, similar_apps=similar_apps)

@app.route('/category/<category_name>')
def category(category_name):
    apps = load_apps()
    # For Premium Unlocked, use special template
    if category_name.lower() == 'premium unlocked' or category_name.lower() == 'premium_unlocked':
        premium_apps = [app for app in apps if app.get('category', '').lower() == 'premium unlocked']
        return render_template('premium_unlocked.html',
                             apps=premium_apps,
                             categories=get_categories())
    # For regular categories, exclude Premium Unlocked apps
    category_apps = [app for app in apps
                    if app.get('category', '').lower() == category_name.lower()
                    and app.get('category', '').lower() != 'premium unlocked']
    return render_template('category.html',
                         category=category_name,
                         apps=category_apps,
                         categories=get_categories())

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    apps = load_apps()
    # By default, exclude Premium Unlocked unless specifically searched
    if query:
        # If searching for "premium" or "unlocked", include Premium Unlocked apps
        if 'premium' in query or 'unlocked' in query or 'mod' in query:
            results = [app for app in apps if
                       query in app.get('name', '').lower() or
                       query in app.get('developer', '').lower() or
                       query in app.get('description', '').lower() or
                       query in app.get('category', '').lower() or
                       query in app.get('mod_features', '').lower()]
        else:
            # Otherwise exclude Premium Unlocked apps
            results = [app for app in apps if
                       (query in app.get('name', '').lower() or
                        query in app.get('developer', '').lower() or
                        query in app.get('description', '').lower() or
                        query in app.get('category', '').lower()) and
                       app.get('category', '').lower() != 'premium unlocked']
    else:
        # Show all regular apps except Premium Unlocked
        results = [app for app in apps if app.get('category', '').lower() != 'premium unlocked']
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

    # Increment download count
    app_data['downloads'] = app_data.get('downloads', 0) + 1
    save_apps(apps)

    # Track download in user's history if logged in
    if current_user.is_authenticated:
        user_id = current_user.id
        if user_id in users_db:
            if 'downloads_history' not in users_db[user_id]:
                users_db[user_id]['downloads_history'] = []

            # Check if already downloaded
            already_downloaded = any(
                d['app_id'] == app_id
                for d in users_db[user_id]['downloads_history']
            )

            if not already_downloaded:
                download_record = {
                    'app_id': app_id,
                    'date': datetime.now().isoformat(),
                    'app_name': app_data.get('name', 'Unknown')
                }
                users_db[user_id]['downloads_history'].append(download_record)

                # FIXED: Use absolute path for cross-platform compatibility
                users_file = os.path.join(project_path, 'users.json')
                with open(users_file, 'w') as f:
                    json.dump(users_db, f, indent=2)

                # Log activity
                log_activity(user_id, 'download', f"Downloaded {app_data.get('name', 'app')}")

    has_file = bool(app_data.get('app_file'))
    return jsonify({
        'success': True,
        'downloads': app_data['downloads'],
        'message': 'Download started!',
        'has_file': has_file,
        'file_url': f'/download/{app_id}' if has_file else None
    })

# استبدل الدالة القديمة بهذه النسخة النهائية بالكامل

@app.route('/download/<app_id>')
def download_file(app_id):
    """
    Handles both external URL redirects and serving local files securely.
    """
    apps = load_apps()
    app_data = next((app for app in apps if app['id'] == app_id), None)

    if not app_data:
        abort(404, description="App not found")

    # --- الجزء الأول: التعامل مع الروابط الخارجية (من تطويرك) ---
    if app_data.get('is_external_download'):
        external_url = app_data.get('download_link') or app_data.get('app_file_path')
        if external_url and external_url.startswith('http'):
            # نقوم بإعادة التوجيه مباشرة إلى الرابط الخارجي
            return redirect(external_url)
        else:
            abort(404, description="External download link is invalid or missing")

    # Handle local file downloads
    app_file = app_data.get('app_file')
    if not app_file:
        abort(404, description="No local file available for this app")

    # FIXED: Use absolute path for cross-platform compatibility
    file_path = os.path.join(project_path, 'Apps_Link', app_file)

    if not os.path.exists(file_path):
        abort(404, description="File not found on the server.")

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        abort(500, description="An error occurred while preparing your download.")

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
        user_data = None
        user_id = None
        for uid, udata in users_db.items():
            if udata['username'] == username:
                user_data = udata
                user_id = uid
                break
        if user_data and check_password_hash(user_data.get('password', ''), password):
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
        for uid, udata in users_db.items():
            if udata['username'] == username:
                flash('Username already exists', 'error')
                return render_template('register.html')
        user_id = str(len(users_db) + 1)
        users_db[user_id] = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'created_at': datetime.now().isoformat()
        }
        # FIXED: Use absolute path for cross-platform compatibility
        users_file = os.path.join(project_path, 'users.json')
        with open(users_file, 'w') as f:
            json.dump(users_db, f, indent=2)
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
    data = request.json
    if not data or not data.get('uid'):
        return jsonify({'error': 'Invalid authentication data'}), 400
    firebase_uid = data['uid']
    email = data.get('email', '')
    display_name = data.get('displayName', '')
    photo_url = data.get('photoURL', '')
    user_id = f"firebase_{firebase_uid}"
    if user_id not in users_db:
        username = display_name if display_name else email.split('@')[0]
        base_username = username
        counter = 1
        while any(u['username'] == username for u in users_db.values()):
            username = f"{base_username}{counter}"
            counter += 1
        users_db[user_id] = {
            'username': username,
            'email': email,
            'password': generate_password_hash(secrets.token_hex(32)),
            'firebase_uid': firebase_uid,
            'display_name': display_name,
            'photo_url': photo_url,
            'created_at': datetime.now().isoformat(),
            'auth_provider': 'firebase',
            'favorites': []
        }
    else:
        users_db[user_id]['display_name'] = display_name
        users_db[user_id]['photo_url'] = photo_url
        users_db[user_id]['last_login'] = datetime.now().isoformat()

    users_file = os.path.join(project_path, 'users.json')
    with open(users_file, 'w') as f:
        json.dump(users_db, f, indent=2)

    user = User(user_id, users_db[user_id]['username'], email)
    login_user(user, remember=True)
    return jsonify({
        'success': True,
        'username': users_db[user_id]['username'],
        'message': 'Authentication synced successfully'
    })

@app.route('/api/firebase-logout', methods=['POST'])
def firebase_logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/favorite/<app_id>', methods=['POST'])
@login_required
def toggle_favorite(app_id):
    if not hasattr(current_user, 'favorites'):
        current_user.favorites = []
    if app_id in current_user.favorites:
        current_user.favorites.remove(app_id)
        favorited = False
    else:
        current_user.favorites.append(app_id)
        favorited = True
    if current_user.id in users_db:
        users_db[current_user.id]['favorites'] = current_user.favorites
        users_file = os.path.join(project_path, 'users.json')
        with open(users_file, 'w') as f:
            json.dump(users_db, f, indent=2)
    return jsonify({'favorited': favorited})

@app.route('/favorites')
@login_required
def favorites():
    apps = load_apps()
    user_favorites = users_db.get(current_user.id, {}).get('favorites', [])
    favorite_apps = [app for app in apps if app['id'] in user_favorites]
    return render_template('favorites.html', apps=favorite_apps)

@app.route('/profile/<user_id>')
def user_profile(user_id):
    if user_id not in users_db:
        abort(404)
    user_data = users_db[user_id]
    apps = load_apps()

    # Fetch user downloads with complete app data
    user_downloads = []
    for download in user_data.get('downloads_history', []):
        app = next((a for a in apps if a['id'] == download['app_id']), None)
        if app:
            user_downloads.append({**app, 'download_date': download['date']})

    # Fetch user favorites with complete app data
    user_favorites = []
    for app_id in user_data.get('favorites', []):
        app = next((a for a in apps if a['id'] == app_id), None)
        if app:
            user_favorites.append(app)

    # Fetch user reviews
    user_reviews = []
    for app in apps:
        for review in app.get('reviews', []):
            if review.get('user_id') == user_id:
                user_reviews.append({**review, 'app_name': app['name'], 'app_icon': app.get('icon'), 'app_id': app['id']})

    # Fetch user collections
    user_collections = [c for c in collections_db.values() if c['user_id'] == user_id]
    for collection in user_collections:
        collection['apps_count'] = len(collection.get('apps', []))
        collection['preview_apps'] = [app for app in apps if app['id'] in collection.get('apps', [])]

    # Fetch user wishlist
    user_wishlist = [app for app in apps if app['id'] in user_data.get('wishlist', [])]

    # Fetch user activities
    user_activities = activities_db.get(user_id, [])

    # Get user settings
    user_settings = user_data.get('settings', {
        'profile_public': True,
        'show_downloads': True,
        'show_collections': True,
        'notify_updates': True,
        'notify_reviews': True,
        'notify_followers': True
    })

    profile_user = {
        'id': user_id,
        'username': user_data['username'],
        'email': user_data['email'],
        'avatar': user_data.get('avatar'),
        'bio': user_data.get('bio', ''),
        'location': user_data.get('location', ''),
        'website': user_data.get('website', ''),
        'joined_date': user_data.get('created_at', '').split('T')[0],
        'downloads_count': len(user_data.get('downloads_history', [])),
        'reviews_count': len(user_reviews),
        'favorites_count': len(user_data.get('favorites', [])),
        'followers_count': len(user_data.get('followers', [])),
        'following_count': len(user_data.get('following', []))
    }

    return render_template('profile.html',
                         user=profile_user,
                         user_downloads=user_downloads,
                         user_favorites=user_favorites,
                         user_reviews=user_reviews,
                         user_collections=user_collections,
                         user_wishlist=user_wishlist,
                         user_activities=user_activities,
                         user_settings=user_settings)

@app.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    data = request.json
    user_id = current_user.id
    if user_id in users_db:
        users_db[user_id]['username'] = data.get('username', users_db[user_id]['username'])
        users_db[user_id]['bio'] = data.get('bio', '')
        users_db[user_id]['location'] = data.get('location', '')
        users_db[user_id]['website'] = data.get('website', '')
        users_file = os.path.join(project_path, 'users.json')
        with open(users_file, 'w') as f:
            json.dump(users_db, f, indent=2)
        log_activity(user_id, 'profile_update', 'Updated profile information')
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'User not found'}), 404

@app.route('/api/wishlist/add/<app_id>', methods=['POST'])
@login_required
def add_to_wishlist(app_id):
    user_id = current_user.id
    if user_id in users_db:
        if 'wishlist' not in users_db[user_id]:
            users_db[user_id]['wishlist'] = []
        if app_id not in users_db[user_id]['wishlist']:
            users_db[user_id]['wishlist'].append(app_id)
            users_file = os.path.join(project_path, 'users.json')
            with open(users_file, 'w') as f:
                json.dump(users_db, f, indent=2)
            log_activity(user_id, 'wishlist_add', f'Added app to wishlist')
            return jsonify({'success': True, 'added': True})
        else:
            return jsonify({'success': True, 'added': False, 'message': 'Already in wishlist'})
    return jsonify({'success': False, 'error': 'User not found'}), 404

@app.route('/api/wishlist/remove/<app_id>', methods=['POST'])
@login_required
def remove_from_wishlist(app_id):
    user_id = current_user.id
    if user_id in users_db:
        if 'wishlist' in users_db[user_id] and app_id in users_db[user_id]['wishlist']:
            users_db[user_id]['wishlist'].remove(app_id)
            users_file = os.path.join(project_path, 'users.json')
            with open(users_file, 'w') as f:
                json.dump(users_db, f, indent=2)
            return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/api/collections/create', methods=['POST'])
@login_required
def create_collection():
    data = request.json
    collection_id = str(uuid.uuid4())
    collection = {
        'id': collection_id,
        'user_id': current_user.id,
        'name': data.get('name', 'Untitled Collection'),
        'description': data.get('description', ''),
        'apps': data.get('apps', []),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'is_public': data.get('is_public', True)
    }
    collections_db[collection_id] = collection
    collections_file = os.path.join(project_path, 'collections.json')
    with open(collections_file, 'w') as f:
        json.dump(collections_db, f, indent=2)
    log_activity(current_user.id, 'collection_create', f'Created collection: {collection["name"]}')
    return jsonify({'success': True, 'collection_id': collection_id})

@app.route('/collection/<collection_id>')
def view_collection(collection_id):
    if collection_id not in collections_db:
        abort(404)
    collection = collections_db[collection_id]
    apps = load_apps()
    collection_apps = [app for app in apps if app['id'] in collection['apps']]
    return render_template('collection.html', collection=collection, apps=collection_apps)

@app.route('/api/user/<user_id>/follow', methods=['POST'])
@login_required
def follow_user(user_id):
    if user_id == current_user.id:
        return jsonify({'success': False, 'error': 'Cannot follow yourself'}), 400
    if user_id not in users_db:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    if 'following' not in users_db[current_user.id]:
        users_db[current_user.id]['following'] = []
    if user_id not in users_db[current_user.id]['following']:
        users_db[current_user.id]['following'].append(user_id)
    if 'followers' not in users_db[user_id]:
        users_db[user_id]['followers'] = []
    if current_user.id not in users_db[user_id]['followers']:
        users_db[user_id]['followers'].append(current_user.id)
    users_file = os.path.join(project_path, 'users.json')
    with open(users_file, 'w') as f:
        json.dump(users_db, f, indent=2)
    log_activity(current_user.id, 'follow', f'Started following {users_db[user_id]["username"]}')
    log_activity(user_id, 'follower', f'{current_user.username} started following you')
    return jsonify({'success': True})

@app.route('/admin')
@admin_required
def admin_dashboard():
    apps = load_apps()
    total_users = len(users_db)
    total_downloads = sum(app.get('downloads', 0) for app in apps)
    total_reviews = sum(len(app.get('reviews', [])) for app in apps)
    all_activities = []
    for user_id, activities in activities_db.items():
        for activity in activities[-10:]:
            all_activities.append({**activity, 'username': users_db.get(user_id, {}).get('username', 'Unknown')})
    all_activities.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return render_template('admin.html',
                         apps=apps,
                         total_users=total_users,
                         total_downloads=total_downloads,
                         total_reviews=total_reviews,
                         recent_activities=all_activities[:50])

@app.route('/api/theme/toggle', methods=['POST'])
def toggle_theme():
    theme = request.json.get('theme', 'light')
    resp = make_response(jsonify({'success': True, 'theme': theme}))
    resp.set_cookie('theme', theme, max_age=365*24*60*60)
    return resp

@app.route('/api/search/suggestions')
def search_suggestions():
    """Real-time search suggestions endpoint for instant search results"""
    query = request.args.get('q', '').lower().strip()

    if not query or len(query) < 2:
        return jsonify({'success': True, 'results': []})

    apps = load_apps()

    # Score-based search for better relevance
    scored_results = []

    for app in apps:
        score = 0
        app_name = app.get('name', '').lower()
        app_developer = app.get('developer', '').lower()
        app_description = app.get('description', '').lower()
        app_category = app.get('category', '').lower()

        # Exact match in name (highest priority)
        if query == app_name:
            score += 100
        # Name starts with query
        elif app_name.startswith(query):
            score += 80
        # Query in name
        elif query in app_name:
            score += 60

        # Developer matches
        if query in app_developer:
            score += 30

        # Category matches
        if query in app_category:
            score += 20

        # Description matches (lowest priority)
        if query in app_description:
            score += 10

        # Boost popular apps slightly
        if app.get('featured', False):
            score += 5

        # Add download popularity factor
        downloads = app.get('downloads', 0)
        if downloads > 10000:
            score += 3
        elif downloads > 1000:
            score += 2
        elif downloads > 100:
            score += 1

        if score > 0:
            scored_results.append({
                'id': app.get('id'),
                'name': app.get('name'),
                'icon': app.get('icon'),
                'developer': app.get('developer'),
                'category': app.get('category'),
                'rating': app.get('rating', 0),
                'price': app.get('price', 0),
                'score': score
            })

    # Sort by score and return top 8 results
    scored_results.sort(key=lambda x: x['score'], reverse=True)
    top_results = scored_results[:8]

    # Remove score from final results
    for result in top_results:
        result.pop('score', None)

    return jsonify({'success': True, 'results': top_results})

@app.route('/api/search/advanced', methods=['POST'])
def advanced_search():
    data = request.json
    apps = load_apps()
    results = apps
    if data.get('query'):
        query = data['query'].lower()
        results = [app for app in results if
                   query in app.get('name', '').lower() or
                   query in app.get('description', '').lower() or
                   query in app.get('developer', '').lower()]
    if data.get('category'):
        results = [app for app in results if app.get('category') == data['category']]
    if data.get('min_rating'):
        results = [app for app in results if app.get('rating', 0) >= float(data['min_rating'])]
    if data.get('max_price') is not None:
        results = [app for app in results if app.get('price', 0) <= float(data['max_price'])]
    sort_by = data.get('sort_by', 'relevance')
    if sort_by == 'rating':
        results.sort(key=lambda x: x.get('rating', 0), reverse=True)
    elif sort_by == 'downloads':
        results.sort(key=lambda x: x.get('downloads', 0), reverse=True)
    elif sort_by == 'date':
        results.sort(key=lambda x: x.get('added_date', ''), reverse=True)
    elif sort_by == 'name':
        results.sort(key=lambda x: x.get('name', ''))
    return jsonify({'success': True, 'results': results[:50]})

@app.route('/compare')
def compare_apps():
    app_ids = request.args.getlist('apps')
    apps = load_apps()
    compare_apps_list = [app for app in apps if app['id'] in app_ids]
    return render_template('compare.html', apps=compare_apps_list)

@app.route('/api/analytics/track', methods=['POST'])
def track_analytics():
    data = request.json
    event_type = data.get('type')
    app_id = data.get('app_id')
    if event_type and app_id:
        today = datetime.now().strftime('%Y-%m-%d')
        analytics_db[app_id][f'{event_type}_{today}'] += 1
        analytics_file = os.path.join(project_path, 'analytics.json')
        with open(analytics_file, 'w') as f:
            json.dump(dict(analytics_db), f, indent=2)
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@app.route('/api/analytics/dashboard/<app_id>')
@admin_required
def analytics_dashboard(app_id):
    app_analytics = dict(analytics_db.get(app_id, {}))
    views_data = []
    downloads_data = []
    for key, value in app_analytics.items():
        if 'view_' in key:
            date = key.replace('view_', '')
            views_data.append({'date': date, 'count': value})
        elif 'download_' in key:
            date = key.replace('download_', '')
            downloads_data.append({'date': date, 'count': value})
    return jsonify({
        'views': views_data,
        'downloads': downloads_data,
        'total_views': sum(v['count'] for v in views_data),
        'total_downloads': sum(d['count'] for d in downloads_data)
    })

@app.route('/api/notifications')
@login_required
def get_notifications():
    notifications = users_db.get(current_user.id, {}).get('notifications', [])
    return jsonify({'notifications': notifications})

@app.route('/api/notifications/mark-read', methods=['POST'])
@login_required
def mark_notifications_read():
    notification_ids = request.json.get('ids', [])
    if current_user.id in users_db:
        notifications = users_db[current_user.id].get('notifications', [])
        for notif in notifications:
            if notif['id'] in notification_ids:
                notif['read'] = True
        users_db[current_user.id]['notifications'] = notifications
        users_file = os.path.join(project_path, 'users.json')
        with open(users_file, 'w') as f:
            json.dump(users_db, f, indent=2)
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/api/review/<app_id>/helpful', methods=['POST'])
@login_required
def mark_review_helpful(app_id):
    data = request.json
    review_id = data.get('review_id')
    apps = load_apps()
    app_data = next((app for app in apps if app['id'] == app_id), None)
    if app_data:
        for review in app_data.get('reviews', []):
            if review.get('id') == review_id:
                if 'helpful_votes' not in review:
                    review['helpful_votes'] = []
                if current_user.id not in review['helpful_votes']:
                    review['helpful_votes'].append(current_user.id)
                    review['helpful_count'] = len(review['helpful_votes'])
                    save_apps(apps)
                    return jsonify({'success': True, 'count': review['helpful_count']})
                else:
                    return jsonify({'success': False, 'message': 'Already voted'})
    return jsonify({'success': False, 'error': 'Review not found'}), 404

@app.route('/api/settings/update', methods=['POST'])
@login_required
def update_settings():
    settings = request.json
    if current_user.id in users_db:
        if 'settings' not in users_db[current_user.id]:
            users_db[current_user.id]['settings'] = {}
        users_db[current_user.id]['settings'].update(settings)
        users_file = os.path.join(project_path, 'users.json')
        with open(users_file, 'w') as f:
            json.dump(users_db, f, indent=2)
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

# --- 6. تشغيل التطبيق ---
if __name__ == '__main__':
    # Set debug=False for production
    app.run(debug=False, host='0.0.0.0', port=5000)

