from requests_html import HTMLSession


GOOGLE_SEARCH_URL = "https://google.com/search"
GOOGLE_SEARCH_PARAM = "q"
GOOGLE_SEARCH_RESULT_WRAPPER_SELECTOR = "div.g"
GOOGLE_SEARCH_RESULT_VIDEO_WRAPPER_SELECTOR = "video-voyager"


def parse_website_search_results(html_elem):
    website_search_result_list = html_elem.find(
        GOOGLE_SEARCH_RESULT_WRAPPER_SELECTOR)

    for website_search_result in website_search_result_list:
        if website_search_result.element.getparent().tag == GOOGLE_SEARCH_RESULT_VIDEO_WRAPPER_SELECTOR:
            continue

        website_link_elem = website_search_result.find("a", first=True)
        website_link = website_link_elem.attrs.get("href")

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

        return {
            "title": website_title,
            "link": website_link
        }


def parse_video_search_results(html_elem):
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

        video_duration = "0:0"

        if video_thumbnail_elem.find("div[role='presentation']", first=True):
            video_duration = video_thumbnail_elem.find(
                "div[role='presentation']",
                first=True
            ).text

        if not all([video_title, video_duration, video_link]):
            continue

        return {
            "title": video_title,
            "duration": video_duration,
            "link": video_link
        }


def main():
    session = HTMLSession()
    search_query = "music video"
    response = session.get(
        url=GOOGLE_SEARCH_URL, params={GOOGLE_SEARCH_PARAM: search_query}
    )

    if response and not hasattr(response, "html"):
        return

    website_search_result_list = parse_website_search_results(response.html)
    video_search_result_list = parse_video_search_results(response.html)


if __name__ == "__main__":
    main()
