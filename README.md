# SilesiasolarEnergyMonitoring

## Introduction

## Installation

## Usage

## BackendAPI

### AuthAPI

*  `/auth/register [POST]` - registering new user

    **Request body**:
    ```json
    {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "strong-password"
    }
    ```
    **Response**:
    ```json
    {
        "user": {
            "id": 3,
            "username": "johndoe",
            "email": "johndoe@example.com"
        },
        "token": "dec96b92e1701189de279b7d0e0f3e5f745e9f187915fa44e624eab1e9583fb7"
    }
    ```
    Token should be keeped, since it's needed to get access to any other endpoints.

* `/auth/login [POST]` - logging in (retrieving token)

    **Request body**:
    ```json
    {
        "username": "johndoe",
        "password": "strong-password"
    }
    ```
    **Response**:
    ```json
    {
        "user": {
            "id": 3,
            "username": "johndoe",
            "email": "johndoe@example.com"
        },
        "token": "19d15140c57767956fcfa2e7d9933de2e44a873d41db2f840450109deda6b667"
    }
    ```
    As you can see, response is identical as in case of registering new user, however every time user is logging, new token is generated and old one is no longer valid.

* `/auth/logout [POST]` - logging out \
    Request body is not needed, one thing you need to provide is token passed by header, by doing this provided token is removed from database and no longer valid.

* `/auth/info [GET]` - retrieving user info, token is needed

   **Response**:
    ```json
    {
        "id": 3,
        "username": "johndoe",
        "email": "johndoe@example.com"
    }
    ```
    
### ManagementAPI

* `/user/locations [GET, POST]`
   * `GET` - get all locations assigned to user 
   
      **Response**:
      ```json
       [
          {
              "id": 2,
              "street": "SunnyStreet",
              "number": "62",
              "city": "SilliconCity",
              "zip_code": "11-420",
              "coord_x": null,
              "coord_y": null,
              "user": 3
          },
          {
              "id": 3,
              "street": "SunnyStreet",
              "number": "64",
              "city": "SilliconCity",
              "zip_code": "11-420",
              "coord_x": null,
              "coord_y": null,
              "user": 3
          }
      ]
       ```
    * `POST` - add new location, user's id needs to belong to user currently logged in
    
       **Request body**:
       ```json
       {
            "user": 2,
            "street": "SunnyStreet",
            "number": "68",
            "city": "SilliconCity",
            "zip_code": "11-420"
       }
       ```
       `coord_x` and `coord_y` fields are optional.
       
       **Response**:
       ```json
       {
            "id": 4,
            "street": "SunnyStreet",
            "number": "68",
            "city": "SilliconCity",
            "zip_code": "11-420",
            "coord_x": null,
            "coord_y": null,
            "user": 2
       }
       ```
   
* `/user/hosts [GET]` - get all hosts assigned to user

   **Response**:
   ```json
   {
        "id": 5,
        "ip": "127.0.0.1",
        "port": 2137,
        "slave_address": 1,
        "description": "blah",
        "user": 2,
        "location": 2,
        "meter": 3
    },
    {
        "id": 7,
        "ip": "127.0.0.1",
        "port": 2138,
        "slave_address": 1,
        "description": "blah",
        "user": 2,
        "location": 2,
        "meter": 3
    }
    ```
 
 * `/meters [GET]` - get all available meter models 
      
   **Response**:
   ```json
   [
      {
          "id": 3,
          "name": "sdm630",
          "type": 2
      },
      {
           "id": 4,
           "name": "sdm660",
           "type": 2
       }
   ]
   ```
    
    
 * `/meters/<int:meter_id>/measurements [GET]` - get all available measurements for certain meter
 
   **Response**:
   ```json
   [
       {
           "measurement": "active_power",
           "type": 1
       },
       {
           "measurement": "voltage_ac",
           "type": 1
       },
       {
           "measurement": "voltage_dc",
           "type": 1
       },
       {
           "measurement": "active_energy_produced",
           "type": 2
       },
       {
           "measurement": "active_energy_consumed",
           "type": 2
       }
   ]
   ```
   
* `/user/hosts/<int:host_id>/measurements [GET, POST]` 
   * `GET` - get measurements assigned to certain host
   
      **Response**:
      ```json
      [
          {
              "id": 5,
              "host": 7,
              "measurement": "voltage_dc"
          },
          {
              "id": 6,
              "host": 7,
              "measurement": "voltage_ac"
          },
          {
              "id": 7,
              "host": 7,
              "measurement": "active_power"
          }
      ]
      ```
   
   * `POST` - assign measurements to certain host
   
      **Request body**:
      ```json
      {
            "measurements": [
               "active_energy_produced",
               "active_energy_consumed"
            ]
      }
      ```

      **Response**:
      ```json
      [
          {
              "id": 8,
              "host": 7,
              "measurement": "active_energy_produced"
          },
          {
              "id": 9,
              "host": 7,
              "measurement": "active_energy_consumed"
          }
      ]
      ```
      
### AdminManagementAPI 

* `/admin/locations [GET, POST]`
   * `GET` - get all locations
   * `POST` - add new location, same request body as for `/user/locations`
   
* `/admin/locations/<int:pk> [GET]` - get location with certain id

* `/admin/hosts [GET, POST]`
   * `GET` - get all hosts
   * `POST` - add new host, note that provided location id must point to location that belongs to user with provided id
   
      **Request body**:
      ```json
      {
           "ip": "127.0.0.1",
           "port": 2282,
           "slave_address": 1,
           "description": "test",
           "user": 1,
           "location": 1,
           "meter": 3
      }
      ```
      
      **Response**:
      ```json
      {
          "id": 8,
          "ip": "127.0.0.1",
          "port": 2282,
          "slave_address": 1,
          "description": "test",
          "user": 1,
          "location": 1,
          "meter": 3
      }
      ```

* `/admin/meters [GET, POST]`
   * `GET` - get all available meters
   * `POST` - add new meter to database
   
      **Request body**:
      ```json
      {
          "name": "sdm330",
          "type": 2
      }
      ```
      
      **Response**:
      ```json
      {
          "id": 5,
          "name": "sdm330",
          "type": 2
      }
      ```
 
 * `/admin/measurements [GET, POST]`
   * `GET` - get all available measurements
   * `POST` - add new measurement to database
   
      **Request body**:
      ```json
      {
         "measurement": "current",
         "type": 1
      }
      ```
      
      **Response**:
      ```json
      {
          "measurement": "current",
          "type": 1
      }
      ```
 
 
 * `/admin/registers [GET, POST]`
   * `GET` - get all available registers
   * `POST` - add new register to database, note that measurement must already exist in database
   
      **Request body**:
      ```json
      {
          "address": 12,
          "measurement": "current",
          "unit": "A",
          "type": 1,
          "function_code": 3,
          "meter": 3
      }
      ```
      
      **Response**:
      ```json {
          "id": 8,
          "address": 12,
          "unit": "A",
          "type": 1,
          "function_code": 3,
          "meter": 3,
          "measurement": "current"
      }
      ```
      
* `/admin/users [GET]` - get all users
* `/admin/users/<int:pk> [GET]` - get certain user
