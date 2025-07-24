from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from transliterate import translit, detect_language
import re

app = Flask(__name__)
CORS(app)  # Frontend bilan ishlash uchun CORS yoqiladi

# Ma'lumotlar bazasi bilan ulanish
def get_db_connection():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# Serial rasm URL'ini generatsiya qilish
def get_photo_url(photo_url, file_id):
    if photo_url and photo_url != 'NULL':
        return photo_url
    return f"https://example.com/photos/{file_id}"  # Haqiqiy URL generatsiya usulini qo'shing

# Frontend shablonini yuklash
@app.route('/')
def index():
    return render_template('index.html', show_404=False)

@app.route('/api/serials/latest', methods=['GET'])
def get_latest_serials():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    c = conn.cursor()
    c.execute('''
        SELECT s.id, s.name, s.file_id, s.photo_url, COUNT(m.id) as episode_count
        FROM serial s
        LEFT JOIN movies m ON s.id = m.serial
        GROUP BY s.id
        ORDER BY s.id DESC
        LIMIT 100
    ''')
    serials = [
        {
            'id': row['id'],
            'title': row['name'] or 'Unknown',
            'episodes': f"{row['episode_count']} Episodes" if row['episode_count'] > 1 else "Movie",
            'poster': get_photo_url(row['photo_url'], row['file_id'])
        } for row in c.fetchall()
    ]
    conn.close()
    return jsonify(serials)

@app.route('/api/serials/oldest', methods=['GET'])
def get_oldest_serials():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    c = conn.cursor()
    c.execute('''
        SELECT s.id, s.name, s.file_id, s.photo_url, COUNT(m.id) as episode_count
        FROM serial s
        LEFT JOIN movies m ON s.id = m.serial
        GROUP BY s.id
        ORDER BY s.id ASC
        LIMIT 100
    ''')
    serials = [
        {
            'id': row['id'],
            'title': row['name'] or 'Unknown',
            'episodes': f"{row['episode_count']} Episodes" if row['episode_count'] > 1 else "Movie",
            'poster': get_photo_url(row['photo_url'], row['file_id'])
        } for row in c.fetchall()
    ]
    conn.close()
    return jsonify(serials)

@app.route('/api/serials/random', methods=['GET'])
def get_random_serials():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    c = conn.cursor()
    c.execute('''
        SELECT s.id, s.name, s.file_id, s.photo_url, COUNT(m.id) as episode_count
        FROM serial s
        LEFT JOIN movies m ON s.id = m.serial
        GROUP BY s.id
        ORDER BY RANDOM()
        LIMIT 100
    ''')
    serials = [
        {
            'id': row['id'],
            'title': row['name'] or 'Unknown',
            'episodes': f"{row['episode_count']} Episodes" if row['episode_count'] > 1 else "Movie",
            'poster': get_photo_url(row['photo_url'], row['file_id'])
        } for row in c.fetchall()
    ]
    conn.close()
    return jsonify(serials)

def normalize_text(text):
    # Kirill-Lotin transliteratsiya
    normalized = text.lower().strip()
    extra = []

    # Kirill → Lotin
    if re.search('[а-яА-Я]', normalized):
        extra.append(translit(normalized, 'ru', reversed=True))

    # Lotin → Kirill
    if re.search('[a-zA-Z]', normalized):
        extra.append(translit(normalized, 'ru'))

    return list(set([normalized] + extra))  # Dublikatlarni yo'q qilish

@app.route('/api/serials/search', methods=['GET'])
def search_serials():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])

    queries = normalize_text(query)
    query_words = []
    for q in queries:
        query_words += q.split()

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    c = conn.cursor()
    try:
        c.execute('''
            SELECT s.id, s.name, s.file_id, s.photo_url, COUNT(m.id) as episode_count
            FROM serial s
            LEFT JOIN movies m ON s.id = m.serial
            GROUP BY s.id
        ''')
        rows = c.fetchall()
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        conn.close()
        return jsonify({'error': 'Database query failed'}), 500
    conn.close()

    serials = [
        {
            'id': row['id'],
            'title': row['name'] or 'Unknown',
            'episodes': f"{row['episode_count']} Episodes" if row['episode_count'] > 1 else "Movie",
            'poster': get_photo_url(row['photo_url'], row['file_id'])
        } for row in rows
    ]

    try:
        matched_serials = []
        seen_ids = set()

        for serial in serials:
            norm_titles = normalize_text(serial['title'])
            score = 0

            for variant in norm_titles:
                for word in query_words:
                    if word in variant:
                        score += 2
                    elif variant.startswith(word):
                        score += 1

            if score >= len(query_words):  # Har bir so'z kamida 1 marotaba mos bo'lishi kerak
                if serial['id'] not in seen_ids:
                    seen_ids.add(serial['id'])
                    matched_serials.append((score, serial))

        matched_serials.sort(key=lambda x: x[0], reverse=True)
        return jsonify([s[1] for s in matched_serials])

    except Exception as e:
        print(f"Search processing error: {e}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/play', methods=['POST'])
def play_serial():
    data = request.get_json()
    serial_id = data.get('id')
    if not serial_id or not isinstance(serial_id, int):
        print(f"Invalid serial ID received: {serial_id}")
        return jsonify({'error': 'Invalid or missing serial ID'}), 400
    try:
        # Serial ID ma'lumotlar bazasida mavjudligini tekshirish
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        c = conn.cursor()
        c.execute('SELECT id FROM serial WHERE id = ?', (serial_id,))
        if not c.fetchone():
            conn.close()
            print(f"Serial ID not found: {serial_id}")
            return jsonify({'error': 'Serial not found'}), 404
        conn.close()
        link = f'https://t.me/pymovibot?start=s{serial_id}'
        print(f"Generated link: {link}")
        return jsonify({'link': link})
    except Exception as e:
        print(f"Error in play_serial: {e}")
        return jsonify({'error': 'Server error'}), 500

# 404 xato sahifasi
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', show_404=True), 404

if __name__ == '__main__':
    app.run(debug=True)