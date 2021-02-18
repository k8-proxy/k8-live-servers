from pydantic import BaseModel, Field

class ScreenshotResponse(BaseModel):
    url     : str = Field(..., title="input url for which screenshot was taken"    )
    png_data: str = Field(..., title="base64 encoded string for the screenshot png")
    result  : str = Field(..., title="result"                                      )
