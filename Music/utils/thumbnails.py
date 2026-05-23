import os
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import config

async def generate_thumbnail(video_id, title, thumbnail_url):
    if not os.path.exists("Music/cache"):
        os.makedirs("Music/cache")

    thumb_path = f"Music/cache/{video_id}.jpg"

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail_url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(thumb_path, mode='wb')
                await f.write(await resp.read())
                await f.close()

    try:
        img = Image.open(thumb_path)
        img = img.resize((1280, 720))

        # Add a dark overlay for glassmorphism effect
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 150))
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)

        draw = ImageDraw.Draw(img)

        # Neon Orange color
        neon_orange = (255, 165, 0)

        # Draw a border
        draw.rectangle([20, 20, 1260, 700], outline=neon_orange, width=10)

        # Draw text (simplified as we don't have custom fonts easily accessible)
        draw.text((100, 300), f"NOW PLAYING", fill=neon_orange)
        draw.text((100, 380), f"{title[:40]}...", fill="white")
        draw.text((100, 600), f"PritiMusic Bot", fill=neon_orange)

        img = img.convert('RGB')
        img.save(thumb_path)
        return thumb_path
    except Exception as e:
        print(f"Thumbnail error: {e}")
        return thumb_path
