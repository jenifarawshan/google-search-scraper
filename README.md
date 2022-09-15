# Google Search Scrapper
This project aims to collect data from Google search

## Features
- Categorize website, social media and video search results
- Store search results in local file system
- Run from command line

## Tech
- [Python](https://python.org)
- [pip](https://pypi.org/project/pip)
- [virtualenv](https://pypi.org/project/virtualenv)
- [click](https://pypi.org/project/click)
- [requests-html](https://pypi.org/project/requests-html)

## Getting started

- Install Python 3
- Install pip

- Install virtualenv
```sh
pip install virtualenv
```

- Create a virtual environment
```sh
virtualenv .venv
```

- Activate the virtual environment
```sh
source .venv/bin/activate
```

- Install the dependencies

```sh
pip install -r requirements.txt
```

Run the script

```sh
python main.py
```

## Example

Search for music videos

```sh
# use -q to pass search query
python main.py -q "music videos"

# use --query to pass query
python main.py --query "top 10 movies"

# use input prompt to pass search query
python main.py

# get help
python main.py --help
```

## Sample output
```json
{
  "q": "music videos",
  "pageOneResultCount": 7,
  "pageOneSocialMediaResultCount": 0,
  "pageOneVideoResultCount": 1,
  "timeTakenInMs": 1652.8818607330322,
  "results": {
    "Social Media": [],
    "Webpages": [
      {
        "Website": "https://vimeo.com",
        "results": [
          {
            "Title": "Music Videos on Vimeo",
            "URL": "https://vimeo.com/categories/music"
          }
        ]
      },
      {
        "Website": "https://en.wikipedia.org",
        "results": [
          {
            "Title": "Music video - Wikipedia",
            "URL": "https://en.wikipedia.org/wiki/Music_video"
          }
        ]
      },
      {
        "Website": "https://www.musicgrotto.com",
        "results": [
          {
            "Title": "25 Best Music Videos of All Time",
            "URL": "https://www.musicgrotto.com/best-music-videos-of-all-time/"
          }
        ]
      },
      {
        "Website": "https://www.rollingstone.com",
        "results": [
          {
            "Title": "The 100 Greatest Music Videos - Rolling Stone",
            "URL": "https://www.rollingstone.com/music/music-lists/best-music-videos-1194411/"
          }
        ]
      },
      {
        "Website": "https://music.apple.com",
        "results": [
          {
            "Title": "Music Videos - Apple Music",
            "URL": "https://music.apple.com/us/genre/music-videos/id31"
          }
        ]
      },
      {
        "Website": "https://www.complex.com",
        "results": [
          {
            "Title": "Latest in Music Videos - Complex",
            "URL": "https://www.complex.com/tag/music-videos"
          }
        ]
      }
    ],
    "Videos": [
      {
        "Website": "https://www.youtube.com",
        "results": [
          {
            "DurationInSeconds": 263,
            "Title": "Dua Lipa - Love Again (Official Music Video)",
            "URL": "https://www.youtube.com/watch?v=BC19kwABFwc"
          },
          {
            "DurationInSeconds": 177,
            "Title": "Alesso, Katy Perry - When I'm Gone (Official Music Video)",
            "URL": "https://www.youtube.com/watch?v=N-4YMlihRf4"
          },
          {
            "DurationInSeconds": 690,
            "Title": "Top 10 Best Music Videos of 2021",
            "URL": "https://www.youtube.com/watch?v=VGOaKLmXUoo"
          },
          {
            "DurationInSeconds": 166,
            "Title": "Imagine Dragons - Bones (Official Music Video)",
            "URL": "https://www.youtube.com/watch?v=TO-_3tck2tg"
          },
          {
            "DurationInSeconds": 1249,
            "Title": "Top 20 Music Videos of the Century (So Far) - YouTube",
            "URL": "https://www.youtube.com/watch?v=-oWeX1CBTV4"
          }
        ]
      }
    ]
  }
}
```

## License

MIT

**Feel free to contribute!**

