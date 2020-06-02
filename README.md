# X Ray Backend Dev

This contains Django and REST FRAMEWORK code for the Backend of the X-Ray Anomaly Detection App.

### API Endpoints implemented :

1. 'xray/' : Returns details on the POSTed **x-ray id**, if the correct **User** is presently signed in.
2. 'user/' : Returns the **username** and the **list of past xray-ids** of the POSTed **user-id** if that **User** is presently signed in.
3. 'login/' : Returns **Auth Token** for the *Username* and *Password* POSTed.
4. 'signup/' : Registers a new user with given *username* and *password*.
5. 'upload/' : Uploads the given *image* and *title* to the current **user profile** and also returns the *predicted outputs.*
6. 'anonupload/' : Uploads the given *image* and *title* and returns the **predicted output.**

Notes/Disclaimers : 

* I'm lazy enough, not to write the entire API documentation :p I'll do it once this comes into application.
* The Django Templates work, but they look pretty bad since, I just made those for testing purposes. No Worries :)