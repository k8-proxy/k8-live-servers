from fastapi                                           import APIRouter
from osbot_browser.browser.Browser_Lamdba_Helper       import Browser_Lamdba_Helper

from k8_live_servers.fastapi.model.screenshot_request  import ScreenshotRequest
from k8_live_servers.fastapi.model.screenshot_response import ScreenshotResponse

router = APIRouter()

@router.post("/screenshot", response_model=ScreenshotResponse, tags=["screenshot"])
async def screenshot_endpoint(request: ScreenshotRequest):
    """
    Take screenshot for the given requests
    * return base64 of screenshot png
    """
    browser_helper = Browser_Lamdba_Helper(request.headless).setup()
    png_data       = browser_helper.get_screenshot_png(url       = request.url,
                                                       full_page = True,
                                                       delay     = request.delay,
                                                       js_code   = request.js_code)
    return {"url": request.url, "png_data": png_data, "result": "OK"}