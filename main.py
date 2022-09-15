from collections import defaultdict
from requests_html import HTMLSession, urlparse
import time


GOOGLE_SEARCH_URL = "https://google.com/search"
GOOGLE_SEARCH_PARAM = "q"
GOOGLE_SEARCH_RESULT_WRAPPER_SELECTOR = "div.g"
GOOGLE_SEARCH_RESULT_VIDEO_WRAPPER_SELECTOR = "video-voyager"


def generate_base_website_url(link):
    parsed_url = urlparse(link)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def parse_website_search_results(html_elem):
    result_dict = defaultdict(list)
    result_list = []
    website_search_result_list = html_elem.find(
        GOOGLE_SEARCH_RESULT_WRAPPER_SELECTOR)

    for website_search_result in website_search_result_list:
        if website_search_result.element.getparent().tag == GOOGLE_SEARCH_RESULT_VIDEO_WRAPPER_SELECTOR:
            continue

        website_link_elem = website_search_result.find("a", first=True)
        website_link = website_link_elem.attrs.get("href")
        base_website_url = generate_base_website_url(website_link)

        website_title = ""

        if website_link_elem.find("h3", first=True):
            website_title = website_link_elem.find("h3", first=True).text
        elif website_search_result.find("h3:last-child", first=True):
            website_title = website_title = website_search_result.find(
                "h3:last-child",
                first=True
            ).text

        if not all([website_title, website_link]):
            continue

        result_dict[base_website_url].append({
            "Title": website_title,
            "URL": website_link
        })

    for k, v in result_dict.items():
        result_list.append({
            "Website": k,
            "results": v
        })

    return result_list


def convert_duration_to_seconds(duration):
    hour, min, sec = map(int, ([0] + duration.split(":"))[-3:])
    return (hour * 3600) + (min * 60) + sec


def parse_video_search_results(html_elem):
    result_dict = defaultdict(list)
    result_list = []
    video_search_result_list = html_elem.find(
        GOOGLE_SEARCH_RESULT_VIDEO_WRAPPER_SELECTOR
    )

    for video_search_result in video_search_result_list:
        video_link_elem = video_search_result.find("a", first=True)
        video_link = video_link_elem.attrs.get("href")

        if video_search_result.find("a[aria-label]", first=True):
            video_thumbnail_elem = video_search_result.find(
                "a[aria-label]",
                first=True
            )
        else:
            video_thumbnail_elem = video_search_result.find(
                "div[aria-hidden='true']",
                first=True
            )

        video_title = ""

        if video_link_elem.find("div[role='heading'] span", first=True):
            video_title = video_link_elem.find(
                "div[role='heading'] span",
                first=True
            ).text
        elif video_link_elem.find("h3", first=True):
            video_title = video_link_elem.find("h3", first=True).text
        base_website_url = generate_base_website_url(video_link)

        video_duration = "0:0"

        if video_thumbnail_elem.find("div[role='presentation']", first=True):
            video_duration = video_thumbnail_elem.find(
                "div[role='presentation']",
                first=True
            ).text

        video_duration_in_seconds = convert_duration_to_seconds(video_duration)

        if not all([video_title, video_duration, video_link]):
            continue

        result_dict[base_website_url].append({
            "DurationInSeconds": video_duration_in_seconds,
            "Title": video_title,
            "URL": video_link
        })

    for k, v in result_dict.items():
        result_list.append({
            "Website": k,
            "results": v
        })

    return result_list


def main():
    time_start = time.time()
    search_query = "aws"
    session = HTMLSession()
    output_dict = {
        "q": search_query,
        "pageOneResultCount": '',
        "pageOneVideoResultCount": '',
        "timeTakenInMS": '',
        "results": {
            "Social Media": [],
            "Webpages": [],
            "Videos": []
        }
    }
    response = session.get(
        url=GOOGLE_SEARCH_URL, params={GOOGLE_SEARCH_PARAM: search_query}
    )

    if response and not hasattr(response, "html"):
        return

    website_search_result_list = parse_website_search_results(response.html)
    video_search_result_list = parse_video_search_results(response.html)

    time_end = time.time()
    total_time_in_ms = (time_end - time_start) * 1000

    output_dict["results"]["Webpages"] = website_search_result_list
    output_dict["results"]["Videos"] = video_search_result_list
    output_dict["pageOneResultCount"] = len(website_search_result_list + video_search_result_list)
    output_dict["pageOneVideoResultCount"] = len(video_search_result_list)
    output_dict["timeTakenInMS"] = total_time_in_ms    


    from pprint import pprint

    pprint(output_dict)


if __name__ == "__main__":
    main()
