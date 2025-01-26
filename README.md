# LIKA-AI-PFE  
**Recommendation System for Live Streaming Platform**  

This repository contains the implementation and documentation of a recommendation system developed for a video and live-streaming platform. The system enhances user engagement by providing personalized content recommendations based on user preferences and interactions.

---

## 📖 Project Overview  

### **Purpose**  
The project focuses on building a recommendation system for the Lika platform to help users discover relevant live streams and videos based on their preferences. This system enhances user experience while supporting content creators.  

### **Features**  
- **Clustering** users with similar preferences.  
- Ranking live and saved videos by relevance.  
- Personalized recommendations for users.  
- Integration with **pre-trained models** and **external APIs**.  

---

## 🛠️ Technologies Used  

- **Programming Language**: Python  
- **Frameworks and Libraries**: Flask, TensorFlow, NumPy, OpenCV, Matplotlib, Scikit-learn  
- **Database**: MySQL  
- **Tools**: Visual Studio Code, Postman, JupyterLab, Git  

---

## 🚀 Getting Started  

### **Prerequisites**  
Ensure you have the following installed:  
- **Python 3.8+**  
- **MySQL**  
- **pip** (Python package installer)  

### **Steps to Run the Project**  
1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/MariemHabouria/recommendationsystem.git
2. Navigate to the Project Folder:
   ```bash
   cd recommendationsystem

3. Install Dependencies:
      ```bash
   pip install -r requirements.txt

4. Configure the Database: Update the database configuration in the config.py file.
5. Start the Flask API Server:
   ```bash
   python app.py
## Project Structure
recommendationsystem/
├── models/       # Pre-trained models
├── api/          # Flask REST API
├── database/     # MySQL scripts and schema
├── notebooks/    # Jupyter Notebooks for experiments
├── static/       # Static files (e.g., images)
└── README.md     # Project documentation
##
📊 System Workflow
User Clustering:
Groups users with similar demographics or preferences.

Video Ranking:
Classifies and ranks videos based on popularity and category.

Recommendations:
Suggests content to users based on their assigned clusters.

##
🤝 Contributors
Mariem Habouria
Rana Bourayou
Special thanks to Pyxis IT and supervisors for their guidance and support.
##
📝 License
This project is licensed under the MIT License. See the LICENSE file for more details.


