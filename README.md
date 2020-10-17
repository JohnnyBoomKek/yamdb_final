![yamdb_workflow Actions Status](https://github.com/JohnnyBoomKek/yamdb_final/workflows/yamdb_workflow/badge.svg)

# YaMDB API&Docker

This learning project is designed to collect user's reviews. Categories go as follows:
    - Movies
    - Books
    - Music

## Getting Started

To have this project up and running on your local machine you need to:
- have docker installed
- clone this repository 
- start the container in the background with: docker-compose up -d 
- The API should be up and running on your localhost:8000

### Prerequisites
To begin operating via the admin panel you must first create a superuser. To do that you need to:
- In terminal execute this command: docker-compose exec web python manage.py createsuperuser 
- Follow the promt and input your email, password etc. 
- Open localhost:8000/admin . Here you can login under the superuser's credentials 

### Registering new users
To register a new user one must follow these steps:
- Send a POST request with your email address as a parameter "email" to /api/v1/auth/email/
- Check your mailbox, copy the confirmation code 
- Send a POST request with your email and confirmation code as parameters. You then should receive a JWT token. Use this token to work with the API. 
More about how JWT tokens work can be found here https://jwt.io/introduction/


## Commands
Full list of commands can be found here localhost:8000/redoc

## Authors

Dima Goncharov and the brilliant minds of all of the contributers to Yandex Praktikum. 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

