# Empyrean
 
 Online Circuit Simulator
 Referenced this Flask Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
 
 Currently only runs SQL-Lite. For deployment on Heroku, changes were made to use Heroku's database. Using own server
 requires different code to use MySQL. Can refer to: 
 https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux

 Steps to deploying own server on Linux
 1. In empyrean-web-master directory, enter "pip install -r requirements.txt" in terminal (can do in virtual environment)
 2. In terminal enter "export FLASK_APP=simulator.py"
 3. In terminal enter "flask run" (if encounter "No user_loader has been insstalled for this LoginManager", just restart server
 by Ctrl+C and then enter "flask run" again)
 4. Access site on http://localhost:5000/ or http://127.0.0.1:5000/