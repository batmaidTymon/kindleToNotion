import os
from typing import List
from notion_client import Client
from ClippingsParser import Clipping

class NotionSync:

    def __init__(self, notion: Client):
        self.notion = notion

    def syncWithNotion(self, clippings: List[Clipping]):
        clippingsByTitle = {}
        for clipping in clippings:
            if clipping.title not in clippingsByTitle:
                clippingsByTitle[clipping.title] = []

            clippingsByTitle[clipping.title].append(clipping)
        parentPage = self.notion.pages.retrieve(os.environ["NOTION_BOOKS_PAGE_ID"])

        children = self.notion.blocks.children.list(parentPage['id'])
        childPageBlocks = [x for x in children['results'] if x['type'] == 'child_page']

        for title, clippings in clippingsByTitle.items():
            bookPage = self.__getOrCreateChildPage(parentPage, title, childPageBlocks)

            for clipping in clippings:
                self.notion.blocks.children.append(
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


    def __getOrCreateChildPage(self, parentPage: dict[str, object], title, childPageBlocks):
        block = [x for x in childPageBlocks if x['child_page']['title'] == title]
        if len(block) > 0:
            return block[0]

        return self.notion.pages.create(
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
