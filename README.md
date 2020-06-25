# X-Ray Anomaly Detection Backend REST FRAMEWORK

This contains **Django REST FRAMEWORK** :sleeping_bed:  code for the Backend of the **X-Ray Anomaly Detection Cross-Platform App**.

[![Generic badge](https://img.shields.io/badge/Django-RESTFRAMEWORK-red.svg)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/Maintained-YES-<COLOR>.svg)](https://shields.io/)

## API Endpoints implemented (Links given, to the detailed documentation) :

1. ['/api/chexray/signup/'](#sign-up) : Registers a new user with given *username* and *password*.
2. ['/api/chexray/login/'](#login) : Returns **Auth-Token** for the *Username* and *Password* POSTed.
3. ['/api/chexray/user/'](#user-details) : Returns the **user-id**, **username** and the **list of past xray-ids** of the presently logged in user.
4. ['/api/chexray/xray/'](#xray-details) : Returns details on the POSTed **x-ray id**, if the correct **User** is presently logged in.
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

So, this returns a ```success``` response, the ```username``` and the generated ```token``` in a JSON Response if the resgistration is successful : 
```
{
    response : "Successfully Signup Up",
    username : <username>,
    token : <tokenkey>
}
```

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
  userid : <user_id>,
  username : <username>,
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

```ENDPOINT : '/api/chexray/user/' | REQUEST TYPE : GET```

This is an Authenticated View and to not have an unauthorized ```401 HTTP_ERROR```, it must be  provided with an ```Authorization Header``` :
```
headers: new HttpHeaders({
            'Authorization': `Token ${tokenkey}`,
            })
```

This returns a JSON Response of the presently logged in user :
```
{
    userid : <user_id>,
    username : <username>,
    pastxrays : <[xray_id_1, xray_id_2, xray_id_3, ...]>
}
```
and the list of **pastxrays** is pre-sorted, on the ```date_posted``` attribute. :wink:

### XRay Details

```ENDPOINT : '/api/chexray/xray/' | REQUEST TYPE : POST```

Returns details on the POSTed **x-ray id**, if the correct **user** is presently logged in.

This is an Authenticated View and to not have an unauthorized ```401 HTTP_ERROR```, it must be  provided with an ```Authorization Header``` containing the tokenkey :
```
headers: new HttpHeaders({
            'Authorization': `Token ${tokenkey}`,
            })
```

This returns a JSON Response of the presently logged in user :
```
{
    id : <xray_id>,
    title : <title>,
    image : <image-link>,
    date_posted : <Django-Date-Time-Field>,
    userperson : <user_id>,
    atelectasis : <probability>,
    cardiomegaly : <probability>,
    consolidation : <probability>,
    edema : <probability>,
    pleural_effusion : <probability>
}
```
If you are not the owner of the X-Ray, the error response will be :
```
{
    response : "You don't have permission to view this.",
}
```

### Authenticated User Upload

```ENDPOINT : '/api/chexray/upload/' | REQUEST TYPE : POST```

Saves the POSTed **image** and **title** and **predictions** to the logged in **user profile** and also returns the **predicted outputs** in a JSON Response. POST body :
```
{
    image : <selected-file>,
    title : <char-field>
}
```

Since, this is an Authenticated View, you'll need a new to speicify an ```Authorization Header``` containing the Token-Key :
```
headers: new HttpHeaders({
            'Authorization': `Token ${tokenkey}`,
            })
```

It saves the model like :
```
serializer = XRaySampleSerializer(xray_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
```

And the JSON Response returned :
```
{
    id : <xray_id>,
    title : <title>,
    image : <image-link>,
    date_posted : <Django-Date-Time-Field>,
    userperson : <user_id>,
    atelectasis : <probability>,
    cardiomegaly : <probability>,
    consolidation : <probability>,
    edema : <probability>,
    pleural_effusion : <probability>
}
```

### Anonymous Upload 

**(The Open-API Endpoint)**

```ENDPOINT : '/api/chexray/anonupload/' | REQUEST TYPE : POST```

This is an Open-API Endpoint, so authentication header isn't necessary. The POST Request Body to be sent :
```
{
    image : <selected-file>,
    title : <char-field>
}
```

And the server, returns the prediction JSON Response :
```
{
    id : <xray_id>,
    title : <title>,
    image : <image-link>,
    date_posted : <Django-Date-Time-Field>,
    userperson : 1,
    atelectasis : <probability>,
    cardiomegaly : <probability>,
    consolidation : <probability>,
    edema : <probability>,
    pleural_effusion : <probability>
}
```
**Future Plans for the OPEN-API Endpoint :**
* Do a free ```Session Authentication``` of the 'developers' before using this endpoint.
* Limit the number of API Requests per session to prevent **DDoS attacks** at this endpoint.



## Notes/Disclaimers : 

* The Django Templates work, but they look pretty bad since, I made those just for the purpose of testing. No Worries  :stuck_out_tongue: 
