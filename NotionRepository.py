import json
import os
from notion_client import Client
from ClippingsParser import Clipping

IMPORT_PAGE_TITLE = 'LastImportStatus'

class NotionRepository:

    def __init__(self, notion: Client):
        self.notion = notion

    def getLastClippingFromNotion(self) -> Clipping:
        parentPage = self.notion.pages.retrieve(os.environ["NOTION_BOOKS_PAGE_ID"])
        children = self.notion.blocks.children.list(parentPage['id'])
        importStatusPages = [x
                             for x in children['results']
                             if x['type'] == 'child_page' and x['child_page']['title'] == IMPORT_PAGE_TITLE]
        importStatusPage = importStatusPages[0] if len(importStatusPages) > 0 else None

        if len(importStatusPage) == 0:
            return None

        for block in self.notion.blocks.children.list(importStatusPage['id'])['results']:
            if block['type'] == 'code':
                return Clipping(**json.loads(block['code']['rich_text'][0]['text']['content']))

    def saveLastClippingToNotion(self, lastClipping: Clipping):

        parentPage = self.notion.pages.retrieve(os.environ["NOTION_BOOKS_PAGE_ID"])
        children = self.notion.blocks.children.list(parentPage['id'])
        importStatusPages = [x
                             for x in children['results']
                             if x['type'] == 'child_page' and x['child_page']['title'] == IMPORT_PAGE_TITLE]
        importStatusPage = importStatusPages[0] if len(importStatusPages) > 0 else None

        if len(importStatusPage) == 0:
            importStatusPage = self.notion.pages.create(
                parent={
                    "type": "page_id",
                    "page_id": parentPage['id'],
                },
                properties={
                    "title": [
                        {
                            "text": {
                                "content": "ImportStatus",
                            }
                        }
                    ]
                }
            )

        for block in self.notion.blocks.children.list(importStatusPage['id'])['results']:
            self.notion.blocks.delete(block['id'])

        jsonString = json.dumps(lastClipping.__dict__, indent=2)
        self.notion.blocks.children.append(
            importStatusPage['id'],
            children=[
                {
                    "code": {
                        "language": "json",
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": jsonString,
                                }
                            }
                        ],
                    }
                }
            ]
        )
