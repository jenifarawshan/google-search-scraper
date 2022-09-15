from collections import defaultdict
from datetime import datetime
import time
import json
import os

import click
from requests_html import HTMLSession, urlparse


GOOGLE_SEARCH_URL = "https://google.com/search"
GOOGLE_SEARCH_PARAM = "q"
GOOGLE_SEARCH_RESULT_WRAPPER_SELECTOR = "div.g"
GOOGLE_SEARCH_RESULT_VIDEO_WRAPPER_SELECTOR = "video-voyager"
SOCIAL_MEDIA_WEBSITES = [
    "twitter.com",
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "reddit.com",
]
DB_DIR_NAME = "Database"


def get_base_website_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def get_root_domain(url):
    return ".".join(urlparse(url).netloc.rsplit(".", 2)[-2:])


def convert_duration_to_seconds(duration):
    hour, min, sec = map(int, ([0] + duration.split(":"))[-3:])
    return (hour * 3600) + (min * 60) + sec


def parse_website_search_results(html_elem):
    result_dict = defaultdict(list)
    social_media_result_list = []
    website_result_list = []

    website_search_result_list = html_elem.find(GOOGLE_SEARCH_RESULT_WRAPPER_SELECTOR)

    for website_search_result in website_search_result_list:
        try:
            if (
                website_search_result.element.getparent().tag
                == GOOGLE_SEARCH_RESULT_VIDEO_WRAPPER_SELECTOR
            ):
                continue

            website_link_elem = website_search_result.find("a", first=True)

            if not website_link_elem:
                continue

            website_link = website_link_elem.attrs.get("href")
            base_website_url = get_base_website_url(website_link)

            website_title = ""

            if website_link_elem.find("h3", first=True):
                website_title = website_link_elem.find("h3", first=True).text
            elif website_search_result.find("h3:last-child", first=True):
                website_title = website_title = website_search_result.find(
                    "h3:last-child", first=True
                ).text

            if not all([website_title, website_link]):
                continue

            result_dict[base_website_url].append(
                {"Title": website_title, "URL": website_link}
            )

        except Exception as e:
            print(getattr(e, "message"), repr(e))
        
    for k, v in result_dict.items():
        result = {"Website": k, "results": v}
        domain = get_root_domain(result["Website"])
        if domain in SOCIAL_MEDIA_WEBSITES:
            social_media_result_list.append(result)
        else:
            website_result_list.append(result)

    return website_result_list, social_media_result_list


def parse_video_search_results(html_elem):
    result_dict = defaultdict(list)
    result_list = []
    video_search_result_list = html_elem.find(
        GOOGLE_SEARCH_RESULT_VIDEO_WRAPPER_SELECTOR
    )

    for video_search_result in video_search_result_list:
        try:

            video_link_elem = video_search_result.find("a", first=True)

            if not video_link_elem:
                continue

            video_link = video_link_elem.attrs.get("href")

            if video_search_result.find("a[aria-label]", first=True):
                video_thumbnail_elem = video_search_result.find("a[aria-label]", first=True)
            else:
                video_thumbnail_elem = video_search_result.find(
                    "div[aria-hidden='true']", first=True
                )

            video_title = ""

            if video_link_elem.find("div[role='heading'] span", first=True):
                video_title = video_link_elem.find(
                    "div[role='heading'] span", first=True
                ).text
            elif video_link_elem.find("h3", first=True):
                video_title = video_link_elem.find("h3", first=True).text
            elif video_link_elem.attrs.get("aria-label"):
                video_title = video_link_elem.attrs.get("aria-label")
            
            base_website_url = get_base_website_url(video_link)

            video_duration = "0:0"

            if video_thumbnail_elem.find("div[role='presentation']", first=True):
                video_duration = video_thumbnail_elem.find(
                    "div[role='presentation']", first=True
                ).text

            video_duration_in_seconds = convert_duration_to_seconds(video_duration)

            if not all([video_title, video_duration, video_link]):
                continue

            result_dict[base_website_url].append(
                {
                    "DurationInSeconds": video_duration_in_seconds,
                    "Title": video_title,
                    "URL": video_link,
                }
            )
        except Exception as e:
            print(getattr(e, "message"), repr(e))

    for k, v in result_dict.items():
        result_list.append({"Website": k, "results": v})

    return result_list


@click.command()
@click.option(
    "--query",
    "-q",
    "search_query",
    type=str,
    prompt="Enter search query",
    help="Search query",
)
def main(search_query):
    time_start = time.time()
    session = HTMLSession()
    output_dict = {
        "q": search_query,
        "pageOneResultCount": "",
        "pageOneVideoResultCount": "",
        "timeTakenInMs": "",
        "results": {"Social Media": [], "Webpages": [], "Videos": []},
    }
    response = session.get(
        url=GOOGLE_SEARCH_URL, params={GOOGLE_SEARCH_PARAM: search_query}
    )

    if response and not hasattr(response, "html"):
        return

    (
        website_search_result_list,
        social_media_search_result_list,
    ) = parse_website_search_results(response.html)
    video_search_result_list = parse_video_search_results(response.html)

    time_end = time.time()
    total_time_in_ms = (time_end - time_start) * 1000

    output_dict["results"]["Webpages"] = website_search_result_list
    output_dict["results"]["Social Media"] = social_media_search_result_list
    output_dict["results"]["Videos"] = video_search_result_list
    output_dict["pageOneResultCount"] = len(
        website_search_result_list
        + social_media_search_result_list
        + video_search_result_list
    )
    output_dict["pageOneSocialMediaResultCount"] = len(social_media_search_result_list)
    output_dict["pageOneVideoResultCount"] = len(video_search_result_list)
    output_dict["timeTakenInMS"] = total_time_in_ms

    file_name = f"{search_query}-{datetime.now().isoformat()}.json"

    os.makedirs(DB_DIR_NAME, exist_ok=True)

    with open(os.path.join(DB_DIR_NAME, file_name), "w") as f:
        json.dump(output_dict, f, indent=2)


if __name__ == "__main__":
    main()
