from PIL import Image, ImageFont, ImageDraw
import io
import aiohttp

class ImageProcessing:
    async def PIL_image_from_url(url):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url)
            uimg = io.BytesIO()
            uimg.write(await resp.read())
            return Image.open(uimg)