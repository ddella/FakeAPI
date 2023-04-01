# Python Virtual Environment Setup (Optionnal)
This section is optionnal. Unless you want to play with the source code, you can just build the container and plys with it.

1. Start by cloning the project and change directory where the source reside:

```sh
gh repo clone ddella/FakeAPI
cd FakeAPI/src
```

2. Create and activate a virtual environment:

```sh
python3.11 -m venv .venv
source .venv/bin/activate
export PYTHONPATH=$PWD
```
>To deactivate the environment, just type `deactivate` in the shell or simply close it.

>Don't forget to export `PYTHONPATH`.

3. Install the necessary modules (make sure you have the latest pip installed):
```sh
pip3 install --upgrade pip
pip3 install fastapi uvicorn pydantic pydantic[email]
```
>**Note**: If you get the following error message, it has nothing to do with Python, Pydantic, or your virtual environment. It's a `zsh` shell error.

    (.venv) user@MacBook src % pip3 install pydantic[email]
    zsh: no matches found: pydantic[email]

To avoid this, you can simply put the argument in quotes like this:
```sh
pip install 'pydantic[email]'
```

4. Create the `requirements.txt` file needed to build the image: 
```sh
pip3 freeze > requirements.txt
```

5. Make sure you're using the right Python interpreter, the one in the virtual environment:
```sh
(.venv) % which python3
```

The result should be something similar to this (your milage may vary 😀):
```
/Users/username/.../.venv/bin/python3
```

6. Start the app with the command:
```sh
python3 main.py
```

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
Daniel Della-Noce - [Linkedin](https://www.linkedin.com/in/daniel-della-noce-2176b622/) - daniel@isociel.com

Project Link: [https://github.com/ddella/FakeAPI](https://github.com/ddella/FakeAPI)
<p align="right">(<a href="#readme-top">back to top</a>)</p>
