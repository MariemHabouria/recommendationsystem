import configparser
from flask import Flask, request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import joblib

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the database configuration values from the file
db_type = config['database']['db_type']
db_host = config['database']['db_host']
db_port = config['database']['db_port']
db_name = config['database']['db_name']
db_user = config['database']['db_user']
db_password = config['database']['db_password']

# Construct the database URL from the configuration values
db_url = f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
# Connect to the database
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# Create the Flask app
app = Flask(__name__)

# Define the database schema
Base = declarative_base()

# Define the User class
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    Age = Column(Integer)
    category1 = relationship('UserVideo', back_populates='user')
    cat_id1 = Column(Integer)
    category2 = relationship('UserVideo', back_populates='user')
    cat_id2 = Column(Integer)
    main_cluster = Column(String)
    subcluster1 = Column(Integer)
    subcluster2 = Column(Integer)

# Define the Video, Category, and UserVideo classes as before

# Load the pre-trained clustering model
clustering_model = joblib.load("user_clustering_model.pkl")

# Function to perform user clustering
def perform_user_clustering(users):
    # Extract the relevant user attributes for clustering
    user_attributes = [[user.Age, user.cat_id1, user.cat_id2] for user in users]

    # Perform user clustering
    main_clusters, subclusters1, subclusters2 = clustering_model.predict(user_attributes)

    # Assign the main clusters and subclusters to the users
    for user, main_cluster, subcluster1, subcluster2 in zip(users, main_clusters, subclusters1, subclusters2):
        user.main_cluster = main_cluster
        user.subcluster1 = subcluster1
        user.subcluster2 = subcluster2

# API endpoint to perform user clustering
@app.route('/api/cluster_users', methods=['POST'])
def cluster_users():
    # Get the user IDs from the request parameters
    user_ids = request.json['user_ids']

    # Query the users from the database
    users = session.query(User).filter(User.user_id.in_(user_ids)).all()

    if users:
        # Perform user clustering
        perform_user_clustering(users)

        # Commit the changes to the database
        session.commit()

        return 'User clustering completed successfully'
    else:
        return 'No users found'

# API endpoint to register user video interactions
@app.route('/api/users/<int:user_id>/videos/<int:video_id>', methods=['POST'])
def register_user_video_interaction(user_id, video_id):
    # Get the interaction details from the request parameters
    likes = int(request.form.get('likes', 0))
    dislikes = int(request.form.get('dislikes', 0))
    watch_time = int(request.form.get('watch_time', 0))

    # Query the user and video from the database
    user = session.query(User).get(user_id)
    video = session.query(Video).get(video_id)

    if user and video:
        # Get the category of the video
        category = video.category

        # Create a new UserVideo object and assign the interaction details
        user_video = UserVideo(user_id=user_id, video_id=video_id, likes=likes, dislikes=dislikes, watch_time=watch_time)
        user.videos.append(user_video)
        video.users.append(user_video)

        # Update the video view count and watch time
        video.views += 1
        video.watch_time += watch_time

        # Update the category statistics
        category.likes += likes
        category.dislikes += dislikes
        category.watch_time += watch_time

        session.commit()

        return 'User video interaction registered successfully'
    else:
        return 'User or video not found'

# Assign categories to the user based on overall interaction with videos
@app.route('/api/users/<int:user_id>/assign_categories', methods=['POST'])
def assign_user_categories(user_id):
    # Query the user from the database
    user = session.query(User).get(user_id)

    if user:
        # Get the user's videos and their categories
        user_videos = user.videos
        category_counts = {}

        # Calculate the category counts based on video interactions
        for user_video in user_videos:
            category = user_video.video.category
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1

        # Find the category with the highest count
        most_frequent_category = max(category_counts, key=category_counts.get)

        # Assign the most frequent category to the user
        user.categories.append(most_frequent_category)

        session.commit()

        return 'User categories assigned successfully'
    else:
        return 'User not found'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
