# LIKA-AI-PFE
# Recommendation System for Live Streaming Platform
This repository contains the implementation and documentation of a recommendation system developed for a video and live-streaming platform. The system aims to enhance user engagement by providing personalized content recommendations based on user preferences and interactions.

📖 Project Overview
Purpose The project focuses on building a recommendation system for the Lika platform. It helps users discover relevant live streams and videos based on their preferences, enhancing their experience while supporting content creators.
Features Clustering users with similar preferences. Ranking live and saved videos by relevance. Personalized recommendations for users. Integration with pre-trained models and APIs.
🛠️ Technologies Used Programming Language: Python Frameworks and Libraries: Flask, TensorFlow, NumPy, OpenCV, Matplotlib, Scikit-learn. Database: MySQL. Tools: Visual Studio Code, Postman, JupyterLab, and Git.
🚀 Getting Started Ensure you have the following installed: Python 3.8+, MySQL, and pip (Python package installer). Clone the repository: git clone https://github.com/MariemHabouria/recommendationsystem.git Navigate to the project folder: cd recommendationsystem Install the required Python libraries: pip install -r requirements.txt Configure the database in the config.py file. Start the Flask API server: python app.py
📂 Project Structure recommendationsystem/ ├── models/ # Pre-trained models ├── api/ # Flask REST API ├── database/ # MySQL scripts and schema ├── notebooks/ # Jupyter Notebooks for experiments ├── static/ # Static files (e.g., images) └── README.md # Project documentation
📊 System Workflow User Clustering: Group users with similar demographics or preferences. Video Ranking: Classify and rank videos by popularity and category. Recommendations: Recommend content based on user clusters.
🤝 Contributors Mariem Habouria Rana Bourayou Special thanks to Pyxis IT and supervisors for their support.
📝 License This project is licensed under the MIT License. See LICENSE for more details.
