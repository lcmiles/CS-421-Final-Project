# CS-429 Final Project

## Project Members: Logan Miles, Abhi Bedi, Faris Khan, Nicholas Fason, Taylor Shirah

### Project Description:
The goal of this project was to develop a full-stack web application for software developers and computer scientists. The project required front end and back end development. For our web application we utilized HTML and CSS to build the user interface, the flask framework to handle routing requests and interactions with the database, a SQL database to store the user data, and various Google Cloud Platform resources to host the web application and its associated data.

### Features:
* User account registration/sign in
* Profile viewing and editing, including entering bio information and uploading profile pictures
* User search functionality
* Posting text, images, or video
* Interactions including likes and comments
* A follower system
* Groups that users can join and share posts in

### Instructions to deploy the Flask app locally:

1. Create a Python virtual environment or download and install [Conda](https://www.anaconda.com/download) and then select it as your interpreter within your IDE.
2. Clone the Git repository. Make sure that the folder you clone the repo into is accessible by the Conda interpreter or the virtual environment.
3. Run the following command to download and install the required Python libraries: `pip install -r requirements.txt`
4. Change `LOCAL_TESTING` variable to `True` at line 15 of app.py.
5. Run the app.py file to start the flask app: `python app.py`
6. The Flask app should begin running on your machine and you can access it at `https://localhost:8080` or the ip address provided in the terminal when the app is started.

### References
https://chatgpt.com/share/3680fc4c-a445-4065-8257-a3f049d3467c
https://www.youtube.com/watch?v=-FWuNnCe73g
https://medium.com/codex/continuously-deploying-a-flask-app-from-a-github-repository-to-google-cloud-run-6f26226539b0
https://www.geeksforgeeks.org/setting-up-google-cloud-sql-with-flask/
https://stackoverflow.com/questions/8160494/how-to-make-a-whole-div-clickable-in-html-and-css-without-javascript
https://stackoverflow.com/questions/34027368/css-text-input-field-not-aligning-top-left
https://stackoverflow.com/questions/14993318/catching-a-500-server-error-in-flask
https://stackoverflow.com/questions/41865214/how-to-serve-an-image-from-google-cloud-storage-using-python-flask
https://help.retentionscience.com/hc/en-us/articles/115003025814-How-To-Build-HTML-for-Conditional-Statements
https://stackoverflow.com/questions/43041253/how-to-set-flask-server-timezone-to-gmt
https://www.javatpoint.com/javascript-domcontentloaded-event
