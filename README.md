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

