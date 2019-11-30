# -*- coding: utf-8 -*-
from core import httptools
from core import scrapertools
from core import servertools
from core.item import Item
from platformcode import logger
host = "http://www.crtvg.es"
def mainlist(item):
    logger.info()
    itemlist = []
    itemlist.append(Item(
        channel = item.channel,
        title = "Destacados",
        action = "listseries",
        url = "http://www.crtvg.es/tvg/programas"
    ))
    itemlist.append(Item(
        channel = item.channel,
        title = "Categorías",
        action = "categorias",
        url = "http://www.crtvg.es/tvg/programas"
    ))
    return itemlist
def categorias(item):
    logger.info()
    itemlist =[]
    data = httptools.downloadpage(item.url).data
    patron = '(?s)<option value="([^"].*?)" >([^<]+).*?'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedurl, scrapedtitle in matches:
        itemlist.append(Item(
            channel = item.channel,
            title = scrapedtitle,
            action = "listseries",
            url = host + "/tvg/programas/categoria/" + scrapedurl
        ))
    return itemlist
def listseries(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron = '(?s)class="listadoimagenes-imagen.*?a href="([^"]+).*?img src="([^"]+).*? alt="([^"]+)'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        itemlist.append(Item(
            channel = item.channel,
            title = scrapedtitle,
            thumbnail = host + scrapedthumbnail,
            url = host + scrapedurl,
            action = "episodes"
        ))
    return itemlist
def episodes(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron = ''
    episodematches