# InstaBot

### Note:
> Dear visitors,
>
> I would like to emphasize that the purpose of this project is solely for educational and learning purposes. It is important to note that scraping data > from Instagram is illegal and against Instagram's policies. If you choose to engage in such activities, it may result in your account being blocked by > Instagram.
>
> To ensure that you stay within Instagram's guidelines, I highly recommend that you read through their policy on data scraping. This will give you a > better understanding of what is and isn't allowed when it comes to scraping data from their platform.
>
> Here's a link to Instagram's policy: https://www.instagram.com/about/legal/terms/api/
>
> Please keep in mind that violating Instagram's policies can have serious consequences, so I urge you to use this project only for educational purposes > and to respect Instagram's policies.
>
> Thank you for your understanding and cooperation.


## Install pakages
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


## Run Project
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
