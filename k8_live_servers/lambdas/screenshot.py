from osbot_aws.apis.shell.Lambda_Shell           import lambda_shell
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper

@lambda_shell
def run(event, context=None):
    headless       = event.get('headless', True )
    url            = event.get('url'            )
    delay          = event.get('delay'          )
    shutdown       = event.get('shutdown', False)
    js_code        = event.get('js_code', None)
    browser_helper = Browser_Lamdba_Helper(headless).setup()
    png_data       = browser_helper.get_screenshot_png(url       = url,
                                                       full_page = True,
                                                       delay     = delay,
                                                       js_code   = js_code)
    if shutdown:
        shutdown_browser(browser_helper)

    return png_data

async def shutdown_browser(browser_helper):
    await browser_helper.api_browser.browser_close()
