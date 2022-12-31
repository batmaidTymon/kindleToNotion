#!/usr/bin/env python3
import os
import shutil
import sys
from time import sleep

from notion_client import Client
from dotenv import load_dotenv
from ClippingsParser import ClippingsParser
from NotionRepository import NotionRepository
from NotionSync import NotionSync
from Diskutil import Diskutil
from MacOS import MacOS

clippingsFileOnKindle = '/Volumes/Kindle/documents/My Clippings.txt'

def watchForKindleConnection():
    diskutil = Diskutil()
    for _ in diskutil.waitForKindleConnection():
        sleep(2)
        copyClippingsFileToIcloud()
        run(clippingsFileOnKindle)


def icloudBackupPath():
    return os.environ['ICLOUD_BACKUP_PATH']


def copyClippingsFileToIcloud():
    # copy file from Kindle to iCloud
    shutil.copyfile(clippingsFileOnKindle, icloudBackupPath())


def run(filePath):
    print('Running')
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    notionSync = NotionSync(notion)
    notionRepo = NotionRepository(notion)

    parser = ClippingsParser()
    clippings = list(parser.parseClippings(filePath))
    lastClipping = clippings[-1]

    lastClippingFromNotion = notionRepo.getLastClippingFromNotion()
    if lastClippingFromNotion is not None:
        # find the index of lastClippingFromNotion in clippings
        lastClippingIndex = clippings.index(lastClippingFromNotion)
        if lastClippingIndex > 0:
            clippings = clippings[lastClippingIndex + 1:]

    MacOS.notify(f'Found {len(clippings)} new clippings')
    if len(clippings) > 0:
        notionSync.syncWithNotion(clippings)
        notionRepo.saveLastClippingToNotion(lastClipping)
        MacOS.notify(f'Clippings synced')

    MacOS.ejectKindle()



if __name__ == '__main__':
    load_dotenv()

    # if commandline contains "watch"
    if len(sys.argv) > 1 and sys.argv[1] == 'watch':
        watchForKindleConnection()
    else:
        run(icloudBackupPath())
