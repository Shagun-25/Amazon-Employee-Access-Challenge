## ML-Model-Flask-Deployment
This is a demo project to elaborate how Machine Learning Models are deployed on production using Flask API

### Project Structure
This project has the following major parts :
1. app.py - This contains Flask APIs that receives employee details through GUI or API calls, predicts the access based on our model and returns it.
2. request.py - This uses requests module to call APIs already defined in app.py and dispalys the returned value.
3. templates - This folder contains the HTML template to allow user to enter employee detail and displays the predicted employee access.

### Running the project
1. Run app.py using below command to start Flask API
```
python app.py
```
By default, flask will run on port 5000.

2. Navigate to URL http://localhost:5000

You should be able to view the homepage with the form.

Enter valid numerical values in all 9 input boxes and hit Predict.

If everything goes well, you should  be able to see the predicted result: Either Access Revoked/ Access Granted on the HTML page!
