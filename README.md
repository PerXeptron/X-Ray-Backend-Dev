# X-Ray Anomaly Detection Backend REST FRAMEWORK

This contains **Django REST FRAMEWORK** :sleeping_bed: code for the Backend of the **X-Ray Anomaly Detection Cross-Platform App**.

[![Generic badge](https://img.shields.io/badge/Django-RESTFRAMEWORK-red.svg)](https://shields.io/)

## API Endpoints implemented (Links given, to the detailed documentation) :

1. ['/api/chexray/signup/'](#sign-up) : Registers a new user with given *username* and *password*.
2. ['/api/chexray/login/'](#login) : Returns **Auth-Token** for the *Username* and *Password* POSTed.
3. ['/api/chexray/user/'](#user-details) : Returns the **user-id**, **username** and the **list of past xray-ids** of the presently logged in user.
4. ['/api/chexray/xray/'](#xray-details) : Returns details on the POSTed **x-ray id**, if the correct **User** is presently signed in.
5. ['/api/chexray/upload/'](#authenticated-user-upload) : Uploads the given *image* and *title* to the current **user profile** and also returns the *predicted outputs.*
6. ['/api/chexray/anonupload/'](#anonymous-upload) : Uploads the given *image* and *title* and returns the **predicted output** anonymously.

## Detailed API Documentation :

### Sign-Up

```ENDPOINT : '/api/chexray/signup/' | REQUEST TYPE : POST```

Registers a new user with given *username* and *password*. ```All of the utilities in this project are written in function based views, with authenticated decorators and CSRF Tokens. ```

```
@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully Signed Up"
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
```

So, this returns a ```success``` response, the ```username``` and the generated ```token``` in a JSON Response if the resgistration is successful.

Two types of standard Django errors that can arise from this :
```
{
  username : "A user with that username already exists"
}
```
or
```
{
  password : "Passwords Must Match"
}
```

### Login

```ENDPOINT : '/api/chexray/login/' | REQUEST TYPE : POST```

Returns **Auth-Token** for the correctly POSTed *Username* and *Password*. For the login part, I've **extended** the inherent Django ```rest_framework.authtoken.views.obtain_auth_token``` to build a ```CustomAuthToken``` **class based view**.

Upon posting the **username** and **password** it'll return a JSON Response :
```
{
  userid : <user_id>
  username : <username>
  token : <tokenkey>
}
```
In case of errors :
```
{
  non_field_errors : <error>
}
```

### User Details

### XRay Details

### Authenticated User Upload

### Anonymous Upload 

**(The Open-API Endpoint)**


## Notes/Disclaimers : 

* The Django Templates work, but they look pretty bad since, I made those just for the purpose of testing. No Worries  :stuck_out_tongue: 
