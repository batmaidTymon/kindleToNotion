import os
from notion_client import Client
from dotenv import load_dotenv

from ClippingsParser import parseClippings
from NotionRepository import NotionRepository

clippingsFile = '/Users/tymon/Library/Mobile Documents/com~apple~CloudDocs/Kindle/My Clippings.txt'


def run():
    notion = Client(auth=os.environ["NOTION_TOKEN"])

    clippings = list(parseClippings(clippingsFile))
    lastClipping = clippings[-1]

    repo = NotionRepository(notion)

    lastClippingFromNotion = repo.getLastClippingFromNotion()
    if lastClippingFromNotion is not None:
        # find the index of lastClippingFromNotion in clippings
        lastClippingIndex = clippings.index(lastClippingFromNotion)
        if lastClippingIndex > 0:
            clippings = clippings[lastClippingIndex + 1:]


    syncWithNotion(clippings, notion)
    repo.saveLastClippingToNotion(lastClipping)


def syncWithNotion(clippings, notion: Client):
    clippingsByTitle = {}
    for clipping in clippings:
        if clipping.title not in clippingsByTitle:
            clippingsByTitle[clipping.title] = []

        clippingsByTitle[clipping.title].append(clipping)
    parentPage = notion.pages.retrieve(os.environ["NOTION_BOOKS_PAGE_ID"])

    children = notion.blocks.children.list(parentPage['id'])
    childPageBlocks = [ x for x in children['results'] if x['type'] == 'child_page']

    for title, clippings in clippingsByTitle.items():
        bookPage = getOrCreateChildPage(notion, parentPage, title, childPageBlocks)

        for clipping in clippings:
            notion.blocks.children.append(
                bookPage['id'],
                children=[
                    {
                        "quote": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": clipping.highlightText,
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": clipping.dateAndLocation,
                                    }
                                }
                            ],
                            "color": "gray"
                        }
                    }
                ]
            )
    return


def getOrCreateChildPage(notion: Client, parentPage: dict[str, object], title, childPageBlocks):

    block = [x for x in childPageBlocks if x['child_page']['title'] == title]
    if len(block) > 0:
        return block[0]

    return notion.pages.create(
        parent={
            "type": "page_id",
            "page_id": parentPage['id'],
        },
        properties={
            "title": [
                {
                    "text": {
                        "content": title,
                    }
                }
            ]
        }
    )


if __name__ == '__main__':
    load_dotenv()
    run()
