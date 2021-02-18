from pydantic import BaseModel, Field

class ScreenshotRequest(BaseModel):
    url      : str  = Field(...         , title="url for screenshot"                                      )
    delay    : int  = Field(default=None, title="Delay in seconds before taking the screenshot"           )
    js_code  : str  = Field(default=None, title="JavaScript code to execute on the page before screenshot")
    headless : bool = Field(default=True, title="Open chrome in headless mode or not"                     )