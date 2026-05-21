import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# --- GET ENVIRONMENT VARIABLES FROM RENDER ---
API_ID = int(os.environ.get("API_ID", 1234567))  
API_HASH = os.environ.get("API_HASH", "your_api_hash_here")  
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token_here")  

bot = Client("anime_bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    welcome_text = (
        "✨ ─── ⋆ 🪐 ⋆ ─── ✨\n"
        "👋 ═𝄆 **𝑾𝒆𝒍𝒄𝒐𝒎𝒆 𝒕𝒐 𝑨𝒏𝒊𝒎𝒆𝑿𝑷𝒍𝒐𝒓𝒆𝒓** 𝄇═\n\n"
        "🧬 *Your ultimate gateway to the anime universe.*\n"
        "I can fetch detailed information about any anime instantly!\n\n"
        "⚙️ ══ **𝑼𝒔𝒂𝒈𝒆 𝑮𝒖𝒊𝒅𝒆** ══\n"
        "» Use `/anime <name>` in PM or Groups.\n"
        "» Example: `/anime Solo Leveling`\n\n"
        "📢 *Add me to your group and grant full permissions to enjoy seamlessly!*"
    )
    await message.reply_text(welcome_text)

@bot.on_message(filters.command("anime"))
async def anime_search(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(
            "⚠️ ── **𝑴𝒊𝒔𝒔𝒊𝒏𝒈 𝑨𝒓𝒈𝒖𝒎𝒆𝒏𝒕** ──\n\n"
            "❌ *Please provide an anime name!*\n"
            "» Example: `/anime Attack on Titan`"
        )
        return

    anime_query = " ".join(message.command[1:])
    status_msg = await message.reply_text("🔍 ── *Searching database... Please wait* ── ⚡")
    api_url = f"https://api.jikan.moe/v4/anime?q={anime_query}&limit=1"
    
    try:
        response = requests.get(api_url).json()
        
        if not response.get("data"):
            await status_msg.edit_text(
                "🗺️ ── **𝑵𝒐𝒕 𝑭𝒐𝒖𝒏𝒅** ──\n\n"
                "😔 *Sorry! Could not find any anime matching your query.*"
            )
            return
            
        anime_data = response["data"][0]
        
        title_english = anime_data.get("title_english") or anime_data.get("title")
        title_japanese = anime_data.get("title_japanese", "N/A")
        anime_type = anime_data.get("type", "N/A")
        episodes = anime_data.get("episodes", "Unknown")
        status = anime_data.get("status", "N/A")
        score = anime_data.get("score", "N/A")
        rating = anime_data.get("rating", "N/A")
        synopsis = anime_data.get("synopsis", "No synopsis available.")
        image_url = anime_data["images"]["jpg"]["large_image_url"]
        
        genres_list = [genre["name"] for genre in anime_data.get("genres", [])]
        genres = ", ".join(genres_list) if genres_list else "N/A"
        
        if len(synopsis) > 550:
            synopsis = synopsis[:550] + "..."

        caption = (
            f"🔮 ─── ❖ **𝑨𝑵𝑰𝑴𝑬  𝑫𝑬𝑻𝑨𝑰𝑳𝑺** ❖ ─── 🔮\n\n"
            f"🎬 🏷️ **𝖳𝗂𝗍𝒍𝒆:** {title_english}\n"
            f"🇯🇵 🎏 **𝖩𝖺𝗉𝖺𝗇𝖾𝗌𝖾:** *{title_japanese}*\n"
            f"⭐️ 🌟 **𝖲𝖼𝗈𝒓𝒆:** `{score} / 10`\n"
            f"📁 🧬 **𝖳𝗒𝗉𝒆:** {anime_type}\n"
            f"🔢 🎞️ **𝖤𝗉𝗂𝒔𝒐𝒅𝒆𝒔:** `{episodes}`\n"
            f"⏳ 📈 **𝖲𝗍𝖺𝗍𝒖𝒔:** {status}\n"
            f"🔞 🛡️ **𝖱𝖺𝗍𝗂𝗇𝗀:** {rating}\n"
            f"🎭 🔮 **𝖦𝖾𝗇𝒓𝒆𝒔:** *{genres}*\n\n"
            f"📝 📜 **𝖲𝗒𝗇𝗈𝗉𝒔𝒊𝒔:**\n_{synopsis}_"
        )

        await status_msg.delete()
        await message.reply_photo(photo=image_url, caption=caption)

    except Exception as e:
        print(f"Error encountered: {e}")
        await status_msg.edit_text(
            "🚨 ── **𝑬𝒓𝒓𝒐𝒓  𝑨𝒍𝒆𝒓𝒕** ──\n\n"
            "⚠️ *An internal error occurred while fetching details. Please try again later!*"
        )

if __name__ == "__main__":
    print("🚀 Telegram Bot Engine Started Successfully on Render!")
    bot.run()