import asyncio
from typing import Optional

from loguru import logger

from PicImageSearch import Google, Network
from PicImageSearch.model import GoogleResponse
from PicImageSearch.sync import Google as GoogleSync

proxies = "http://127.0.0.1:1081"
# proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test03.jpg"
file = "images/test03.jpg"


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies) as client:
        google = Google(client=client)
        # resp = await google.search(url=url)
        resp = await google.search(file=file)
        show_result(resp)
        resp2 = await google.next_page(resp)
        show_result(resp2)
        resp3 = await google.pre_page(resp2)  # type: ignore
        show_result(resp3)


@logger.catch()
def test_sync() -> None:
    google = GoogleSync(proxies=proxies)
    resp = google.search(url=url)
    # resp = google.search(file=file)
    show_result(resp)  # type: ignore
    resp2 = google.next_page(resp)  # type: ignore
    show_result(resp2)  # type: ignore
    resp3 = google.pre_page(resp2)  # type: ignore
    show_result(resp3)  # type: ignore
    show_result(resp2)  # type: ignore


def show_result(resp: Optional[GoogleResponse]) -> None:
    if not resp:
        return
    # logger.info(resp.origin)  # Original Data
    logger.info(resp.pages)
    logger.info(len(resp.pages))
    logger.info(resp.url)
    # Should start from index 2, because from there is matching image
    # logger.info(resp.raw[2].origin)
    logger.info(resp.page_number)
    logger.info(resp.raw[2].thumbnail)
    logger.info(resp.raw[2].title)
    logger.info(resp.raw[2].url)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    # test_sync()
