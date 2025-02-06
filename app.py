from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Пример данных пользователей
users = [
    {"id": 1, "name": "Alice", "photo": "https://example.com/alice.jpg"},
    {"id": 2, "name": "Bob", "photo": "https://example.com/bob.jpg"}
]

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/like', methods=['POST'])
def like():
    user_id = request.json.get('userId')
    print(f"User liked: {user_id}")
    return jsonify({"status": "success"})

@app.route('/dislike', methods=['POST'])
def dislike():
    user_id = request.json.get('userId')
    print(f"User disliked: {user_id}")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)