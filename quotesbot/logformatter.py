from __future__ import annotations

import logging
import os
from typing import  Any, Dict, Optional, Union

from twisted.python.failure import Failure

from scrapy import Request, Spider
from scrapy.http import Response
from scrapy import logformatter


SCRAPEDMSG = "TEST Scraped from %(src)s" + os.linesep + "%(item)s"
DOWNLOADERRORMSG_SHORT = "TEST Error downloading %(request)s"
DOWNLOADERRORMSG_LONG = "TEST Error downloading %(request)s: %(errmsg)s"


class CrawlLogFormatter(logformatter.LogFormatter):
    def scraped(
        self, item: Any, response: Union[Response, Failure], spider: Spider
    ) -> dict:
        src: Any
        if isinstance(response, Failure):
            src = response.getErrorMessage()
        else:
            src = response
        return {
            "level": logging.INFO,
            "msg": SCRAPEDMSG,
            "args": {
                "src": src,
                "item": item,
            },
        }

    def download_error(
        self,
        failure: Failure,
        request: Request,
        spider: Spider,
        errmsg: Optional[str] = None,
    ) -> dict:
        args: Dict[str, Any] = {"request": request}
        if errmsg:
            msg = DOWNLOADERRORMSG_LONG
            args["errmsg"] = errmsg
        else:
            msg = DOWNLOADERRORMSG_SHORT
        return {
            "level": logging.ERROR,
            "msg": msg,
            "args": args,
        }
