<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

# What is FakeAPI

FakeAPI is a Python script that implements most of the REST API methods. Do not use it in a production deployment. The script does almost no testing to keep the code small.

Doesn't implement XML, returns JSON objects only.

The script requires the following modules:
* pydantic
* uvicorn
* fastapi

REST API methods implemented:
* **HTTP GET** to retrieve information
* **HTTP POST** to create a new resource
* **HTTP PUT** to Update/Replace a resource
* **HTTP DELETE** to delete a resource
* **HTTP PATCH** to make a Partial Update/Modify

# How to use this image
## This is for educationnal **only**!

## Build the image with the Dockerfile in your Python app project
This is my `Dockerfile`:

    FROM python:alpine

    RUN ["mkdir", "-p", "/usr/src/data"]
    WORKDIR /usr/src/app

    COPY ["requirements.txt", "./"]
    RUN ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]

    COPY ["./FakeREST_API.py", "./"]

    EXPOSE 8000

    CMD [ "python", "./FakeREST_API.py" ]

After the build, the imaage should be `~78Mb`.

```sh
docker build -t fakeapi .
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Run the project with the data file inside the container.
The data will be lost when the container exits.
```sh
docker run -it --rm -p 8000:8000 --name fakeapi fakeapi
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Run the project with the data file on the Docker host.
Mount the container `/usr/src/data` directory on the current directory of the host. Data will be on the Docker host when the container exits.
```sh
docker run -it --rm -v $PWD:/usr/src/data -p 8000:8000 --name fakeapi fakeapi
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Shell access
Get shell access to the container with the `/usr/src/data` directory mounted on the current directory of the host.
```sh
docker run -it --rm -v $PWD:/usr/src/data fakeapi /bin/sh
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE.txt` for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
Daniel Della-Noce - [Linkedin](https://www.linkedin.com/in/daniel-della-noce-2176b622/) - daniel@isociel.com

Project Link: [https://github.com/ddella/FakeAPI](https://github.com/ddella/FakeAPI)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* [Official documentation of FastAPI](https://fastapi.tiangolo.com/)
* [Real Python tutorial](https://realpython.com/fastapi-python-web-apis/#learn-more-about-fastapi)
* [REST API status code](https://restfulapi.net/http-status-codes/)
* [REST API method](https://restfulapi.net/http-methods/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template/pull/73)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

