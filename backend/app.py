import os
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import MySQLdb
from MySQLdb import Error

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DATABASE_HOST', 'db'),
    'port': int(os.getenv('DATABASE_PORT', 3306)),
    'user': os.getenv('DATABASE_USER', 'fridgie_user'),
    'passwd': os.getenv('DATABASE_PASSWORD', 'fridgie_password'),
    'db': os.getenv('DATABASE_NAME', 'fridgie')
}

def get_db_connection():
    """Create and return a database connection."""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connection = MySQLdb.connect(**DB_CONFIG)
            return connection
        except Error as e:
            print(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise

@app.route('/')
def index():
    """Root endpoint."""
    return jsonify({
        'message': 'Welcome to Fridgie API',
        'version': '1.0.0',
        'endpoints': {
            '/': 'This help message',
            '/health': 'Health check',
            '/api/items': 'Get all items (GET) or create item (POST)',
            '/api/items/<id>': 'Get, update (PUT) or delete (DELETE) specific item'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        conn.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 503

@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, quantity, created_at FROM items ORDER BY created_at DESC')
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        items_list = [
            {
                'id': item[0],
                'name': item[1],
                'quantity': item[2],
                'created_at': item[3].isoformat() if item[3] else None
            }
            for item in items
        ]
        
        return jsonify(items_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items', methods=['POST'])
def create_item():
    """Create a new item in the database."""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400
        
        name = data['name']
        quantity = data.get('quantity', 1)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO items (name, quantity) VALUES (%s, %s)',
            (name, quantity)
        )
        conn.commit()
        item_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return jsonify({
            'id': item_id,
            'name': name,
            'quantity': quantity,
            'message': 'Item created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, name, quantity, created_at FROM items WHERE id = %s',
            (item_id,)
        )
        item = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if item:
            return jsonify({
                'id': item[0],
                'name': item[1],
                'quantity': item[2],
                'created_at': item[3].isoformat() if item[3] else None
            }), 200
        else:
            return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        updates = []
        params = []
        
        if 'name' in data:
            updates.append('name = %s')
            params.append(data['name'])
        
        if 'quantity' in data:
            updates.append('quantity = %s')
            params.append(data['quantity'])
        
        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        params.append(item_id)
        query = f"UPDATE items SET {', '.join(updates)} WHERE id = %s"
        
        cursor.execute(query, params)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Item updated successfully'}), 200
        else:
            return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item by ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Item deleted successfully'}), 200
        else:
            return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
