# Powerplant-coding-challenge

## Introduction

This app computes the distribution of power for the engie powerplant-challenge using Python 3.6.5 and flask.
The entire code is located in the `powerplant_api.py` file. In order to run the app follow these steps:

## Requirements

Make sure to have python 3.6.5 or higher and install flask as well as numpy. The details can be found in the `requirements.txt` file.
I tested the app using the latest version of [Postman](https://www.postman.com/downloads/).

## Running the app

Clone the git directory and navigate your command line to it, then run the app via:

```python powerplant_api.py```

The command line will return a url, copy the url and append `productionplan` in the Postman app in a new tab.
Select POST left of the url box and click on the body radio button. Select raw, then JSON format on the right.
Paste your json file contents in the box under the buttons and hit the Send button on the right of the url box.

The response json will then be sent back as per the requirements of the coding challenge.

Alternatively the code contains unit tests which are commented out in the in main function. These can be used to test out the provided test payloads in the command line.
