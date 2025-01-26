import configparser
import cv2
import os
import numpy as np
import collections
from flask import Flask, request
from tensorflow.keras.models import load_model
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import time

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the database configuration values from the config.ini file
db_type = config['database']['db_type']
db_host = config['database']['db_host']
db_port = config['database']['db_port']
db_name = config['database']['db_name']
db_user = config['database']['db_user']
db_password = config['database']['db_password']
# URL
db_url = f'{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
# Connect to the database
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# Create the Flask app
app = Flask(__name__)

# Define the database 
Base = declarative_base()
# create class video
class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    live = Column(Boolean, default=False)
    views = Column(Integer)
    rank = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='videos')
    final_category = Column(String(50))
# create class category
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    videos = relationship('Video', back_populates='category')

# Load model
model = load_model('classifier.h5')

# Define the categories
categories = {'art': 0, 'beauty': 1, 'Chatting': 2, 'cooking': 3, 'education': 4, 'gaming': 5, 'music': 6, 'news': 7, 'others': 8, 'sports': 9}

#  extract frames from a video and classify them
def extract_frames_and_classify(video_path, category):
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "Error opening video file"
    
    # for live streaming
    current_time = 0
    current_frame = 0

    if cap.get(cv2.CAP_PROP_POS_AVI_RATIO) < 1:
        start_time = time.time()
        duration = 10  # Duration to take frames from live video: 10 minutes
        
        start_time = time.time()
        while time.time() - start_time < duration * 60:  # seconds
            ret, frame = cap.read()
            classify(ret, frame, category)  
            
   

    #saved videos
    frames = []  # List to store selected categories
    max_frames = 100 #max_frames
    frame_count = 0

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        classify(frame, frames, category)
        frame_count += 1

    cap.release()

    counter = collections.Counter(frames)
    most_frequent_category = counter.most_common(1)[0][0]
    
    session = Session()
    video = session.query(Video).filter_by(title=video_path).first()
    video.final_category = most_frequent_category
    session.commit()
    session.close()
    

def classify(frame, frames, category):
    resized_frame = cv2.resize(frame, (70, 70))
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    normalized_frame = gray_frame / 255.0
    frame_input = normalized_frame.reshape(-1, 70, 70, 1)
    predictions = model.predict(frame_input)

    selected_indices = np.argmax(predictions, axis=1)
    selected_categories = [categories[i+1] for i in selected_indices]
    category_path = os.path.join(config['Directories']['categories_directory'], category)
    if not os.path.exists(category_path):
        os.makedirs(category_path)
    frames.extend(selected_categories)

# Define API endpoint 
@app.route('/extract_and_classify_frames', methods=['POST'])
def extract_and_classify_frames():
    # Get video path and category from request parameters
    video_path = request.form.get('video_path')
    category = request.form.get('category')

# extract frames function
    extract_frames_and_classify(video_path, category)



# Define the API endpoint for updating video ranks
@app.route('/api/categories/<int:category_id>/videos/rank', methods=['PUT'])
def update_video_rank(category_id=None):
    # get category
    session = Session()
    category = session.query(Category).get(category_id)

    # get videos from each category
    videos = category.videos

# live / saved
    live_videos = [video for video in videos if video.live]
    saved_videos = [video for video in videos if not video.live]

    # Sort saved videos based on the views
    sorted_saved_videos = sorted(saved_videos, key=lambda x: x.views, reverse=True)

    # Update the rank attribute of each video: positioned first in the category
    for i, video in enumerate(live_videos):
        video.rank = i + 1

    # Update the rank attribute of each saved video: positioned after the live videos
    for i, video in enumerate(sorted_saved_videos, start=len(live_videos)):
        video.rank = i + 1

    # Save the updated videos back to the database
    session.commit()
    session.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

