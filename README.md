# InstaBot

## Installing pakages

Install **[pipenv](https://pypi.org/project/pipenv/)**

```console
pip install pipenv
```

Run following commands inside project dir
```console
pipenv shell
```
Above command creates and activates virtualenv

To install application packages run following command

```console
pipenv install
```


## Running Project
`main.py` must be executed to run the project. 
```console
python main.py
```


## Features
- Sending personal messages to users
- Searching hashtags and adding Like & comment on posts



## Code Details

Import `InstaBot` class and initialize it and set these env variables `INSTA_USERNAME`,  `INSTA_PASSWORD` check [example.env](example.env) file for more information.

```python
from instabot import InstaBot

bot = InstaBot()
```

To send personal messages to users run following method
before running this method you've to set `INSTA_USERNAMES` env variable
it contain usersnames seprated by "`,`".

```python
bot.send_personal_messages()
```

The following method likes popular posts of the provided hashtags in `INSTA_HASHTAGS`.

```python
bot.like_hashtag_posts()
```

The following method comments on popular posts of the provided hashtags in `INSTA_HASHTAGS`.

```python
bot.comment_hashtag_posts()
```

The following method comments & likes on popular posts of the provided hashtags in `INSTA_HASHTAGS`.

```python
bot.like_and_comment_hashtag_posts()
```
