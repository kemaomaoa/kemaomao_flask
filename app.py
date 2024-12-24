from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

db.create_all()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    scores = db.relationship('Score', backref='player', lazy=True)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    game_date = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/')
def index():
    return render_template('index.html')  # 确保你的前端文件名为index.html

@app.route('/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([{'id': player.id, 'username': player.username, 'scores': [score.score for score in player.scores]} for player in players])

@app.route('/players/<int:player_id>/scores', methods=['POST'])
def add_score(player_id):
    score = request.json.get('score')
    if not score:
        return jsonify({'error': 'Score is required'}), 400
    new_score = Score(player_id=player_id, score=score)
    db.session.add(new_score)
    db.session.commit()
    return jsonify({'message': 'Score added successfully'}), 201


if __name__ == "__main__":
    app.run(debug=True)