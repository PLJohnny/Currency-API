# Currency API

## Overview
This project was created as a part of a recruitment process.

The idea was to fetch all the currency exchange rate data from https://www.ecb.europa.eu/home/html/rss.en.html and expose it as a REST API using Python, and preferably Django.

I used Django 3 (this was my first time using it) with Django Rest Framework. I tried to keep my dependency list as short as possible so as not to confuse anyone with code that heavily relies on some library's specific way of doing things. That's why I parsed the RSS urls from raw HTML using regex and that's why I employed DRF's serializers to parse the RSS streams. I only had to install REST Framework XML to get access to the XMLParser.

## Challenges
I wanted to start things out using TDD. I pretty much knew what my REST API would look like so I tried to write tests that would ensure that this idea turns into reality without any issues. Unfortunately, I usually don't have the luxury of having enough time to do TDD, so I'll call it a challenge, even though it turned out pretty nicely (even if the tests themselves are not too complicated - I only had 3 hours after all).

Another challenge was RSS parsing. I didn't know too much about the format, other than the fact that it's a subset of XML. It turned out the XMLParser I used prefixed keys with RDF statements, so I wrote a recursive function that fixed it. I also stumbled upon an issue with the same element (item) being repeated multiple times in the RSS. The XMLParser had the logic required to handle such a case, but wasn't cutting it when it came to actually recognizing that it had to run this logic. I simply made my own inherited parser that overrode a small part of the original code to make it work.

A minor challenge was finding out why REST Framework XML broke, claiming I had no `six` installed. It turned out the library hasn't been updated to work with Django 3 yet, but I found a repository that had already fixed the issue and submitted a PR. It will have to reside in my project's requirements until the official repository maintainer merges the PR.

## What I didn't do
I initially wanted to hook up the task that would fetch latest exchange rate data for all currencies to Celery and set it up as a periodic task that would run every day. Unfortunately after spending around 10 minutes trying to figure out why the Celery worker falls into an infinite recursion loop after starting I decided to just move on and wrote the currency info fetching utility as a Django management command.

This could still work in a production environment - it would just a be a matter of adding the management command to crontab.

## Installation

Create a virtual environment and activate it

```bash
virtualenv env -p python3
source env/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

Create a `.env` file
```bash
touch .env
```
For a minimal configuration, you'll have to supply two variables in the `.env`. It could look like this:
```bash
SQLITE = 1
SECRET_KEY = _
```
(if you'd like to use a DB different than SQLITE, omit the SQLITE variable and supply the variables as prompted when trying to run the app)

Run migrations
```bash
./manage.py migrate
```

## Loading data
I have prepared a management command that will populate the database with all the currencies available at https://www.ecb.europa.eu/home/html/rss.en.html

```bash
./manage.py fetch_latest_currency_data
```

## Running the project

```bash
./manage.py runserver
```

you will find a convenient browsable API at http://127.0.0.1:8000/api/.
