from requests_html import HTMLSession


def main():
    session = HTMLSession()
    response = session.get(
        url="https://google.com/search", params={"q": "music video"})

    if response and not hasattr(response, "html"):
        return

    website_search_result_list = response.html.find("div.g")

    for website_search_result in website_search_result_list:
        if website_search_result.element.getparent().tag == "video-voyager":
            continue

        website_link_elem = website_search_result.find("a", first=True)
        website_link = website_link_elem.attrs.get("href")

        website_title = ""

        if website_link_elem.find("h3", first=True):
            website_title = website_link_elem.find("h3", first=True).text
        elif website_search_result.find("h3:last-child", first=True):
            website_title = website_title = website_search_result.find(
                "h3:last-child", first=True).text

        if not all([website_title, website_link]):
            continue

        print(website_title, website_link)

    video_search_result_list = response.html.find("video-voyager")

    for video_search_result in video_search_result_list:
        video_link_elem = video_search_result.find("a", first=True)
        video_link = video_link_elem.attrs.get("href")

        if video_search_result.find("a[aria-label]", first=True):
            video_thumbnail_elem = video_search_result.find(
                "a[aria-label]", first=True)
        else:
            video_thumbnail_elem = video_search_result.find(
                "div[aria-hidden='true']", first=True)

        video_title = ""

        if video_link_elem.find("div[role='heading'] span", first=True):
            video_title = video_link_elem.find(
                "div[role='heading'] span", first=True).text
        elif video_link_elem.find("h3", first=True):
            video_title = video_link_elem.find("h3", first=True).text

        video_duration = "0:0"

        if video_thumbnail_elem.find("div[role='presentation']", first=True):
            video_duration = video_thumbnail_elem.find(
                "div[role='presentation']", first=True).text

        if not all([video_title, video_duration, video_link]):
            continue

        print(video_title, video_duration, video_link)


if __name__ == "__main__":
    main()
