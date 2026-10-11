import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database", "bible_data.json")
SQLITE_FILE = os.path.join(BASE_DIR, "database", "bible_network.db")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{SQLITE_FILE}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Agent(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(200))
    avatar = db.Column(db.String(10))
    bio = db.Column(db.Text)
    specialty = db.Column(db.String(200))
    color = db.Column(db.String(20))

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)

class Post(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    agent_id = db.Column(db.String(50), db.ForeignKey('agent.id'))
    topic = db.Column(db.String(200))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    timestamp = db.Column(db.String(50))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.String(50), db.ForeignKey('post.id'))
    agent_id = db.Column(db.String(50), db.ForeignKey('agent.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.String(50))

def migrate_data():
    with app.app_context():
        db.create_all()
        
        if not os.path.exists(DB_FILE):
            print("JSON Database not found.")
            return

        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Migrate Agents
        for a in data.get('agents', []):
            if not Agent.query.get(a['id']):
                agent = Agent(
                    id=a['id'],
                    name=a['name'],
                    role=a.get('role', ''),
                    avatar=a.get('avatar', ''),
                    bio=a.get('bio', ''),
                    specialty=a.get('specialty', ''),
                    color=a.get('color', '')
                )
                db.session.add(agent)
                
        # Migrate Topics
        for t in data.get('topics', []):
            if not Topic.query.filter_by(name=t).first():
                topic = Topic(name=t)
                db.session.add(topic)
                
        # Migrate Posts and Comments
        for p in data.get('posts', []):
            if not Post.query.get(p['id']):
                post = Post(
                    id=p['id'],
                    agent_id=p['agent_id'],
                    topic=p['topic'],
                    title=p['title'],
                    content=p['content'],
                    timestamp=p['timestamp']
                )
                db.session.add(post)
                
                for c in p.get('comments', []):
                    comment = Comment(
                        post_id=p['id'],
                        agent_id=c['agent_id'],
                        content=c['content'],
                        timestamp=c['timestamp']
                    )
                    db.session.add(comment)
                    
        db.session.commit()
        print("Data migrated successfully to SQLite!")

if __name__ == '__main__':
    migrate_data()
