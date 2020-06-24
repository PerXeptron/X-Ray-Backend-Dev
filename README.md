# X-Ray Anomaly Detection Backend REST FRAMEWORK

This contains **Django REST FRAMEWORK** :sleeping_bed: code for the Backend of the **X-Ray Anomaly Detection Cross-Platform App**.

## API Endpoints implemented (Links given, to the detailed documentation) :

1. ['/api/chexray/signup/'](#sign-up) : Registers a new user with given *username* and *password*.
2. ['/api/chexray/login/'](#login) : Returns **Auth-Token** for the *Username* and *Password* POSTed.
3. ['/api/chexray/user/'](#user-details) : Returns the **user-id**, **username** and the **list of past xray-ids** of the presently logged in user.
4. ['/api/chexray/xray/'](#xray-details) : Returns details on the POSTed **x-ray id**, if the correct **User** is presently signed in.
5. ['/api/chexray/upload/'](#authenticated-user-upload) : Uploads the given *image* and *title* to the current **user profile** and also returns the *predicted outputs.*
6. ['/api/chexray/anonupload/'](#anonymous-upload) : Uploads the given *image* and *title* and returns the **predicted output** anonymously.

## Detailed API Documentation :

### Sign-Up

### Login

### User Details

### XRay Details

### Authenticated User Upload

### Anonymous Upload 

**(The Open-API Endpoint)**


Notes/Disclaimers : 

* The Django Templates work, but they look pretty bad since, I just made those for testing purposes. No Worries :)
