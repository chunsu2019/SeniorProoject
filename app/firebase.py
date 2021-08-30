import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBXvkA0HPuhwmLTRYYWMS4xCfzC5kV5dY4",
  "authDomain": "health-d48d4.firebaseapp.com",
  "databaseURL": "https://health-d48d4-default-rtdb.firebaseio.com",
  "projectId": "health-d48d4",
  "storageBucket": "health-d48d4.appspot.com",
  "messagingSenderId": "736543335248",
  "appId": "1:736543335248:web:b32dda35a874aba8140255",
  "measurementId": "G-KSL3Y4SZYK"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login(email, password):
  try: 
    auth.sign_in_with_email_and_password(email, password)
    print("inside login", email, password)
    return True
  except:
    print("Invalid email or password")
    print("inside login", email, password)
    return False
  
def createAccount(email, password):
  try:
    auth.create_user_with_email_and_password(email, password)
    return True
  except:
    return False
    
def logout():
  auth.current_user = None
  print("signout")

def isLoggedIn():
  if auth.current_user:
    print("LoggedIn")
    return True
  else:
    print("Not Logged In")
    return False
        
def getUID():
  if auth.current_user:
    return auth.current_user["localId"]
  else:
    return (0)  