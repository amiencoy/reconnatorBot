import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Import modul-modul yang sudah kita buat sebelumnya
from modules.crtsh_fetcher import fetch_subdomains
from modules.otx_fetcher import fetch_subdomains_otx
from modules.http_prober import probe_subdomains
from modules.attack_engine import run_nuclei

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=bot_token)
dp = Dispatcher()

# Global Dictionary untuk menyimpan status lock & task per sesi (chat_id)
active_sessions = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Reconnator standby. Use /scan <target> to begin.")

@dp.message(Command("scan"))
async def cmd_scan(message: types.Message):
    chat_id = message.chat.id
    
    # 1. FITUR LOCK & CANCEL
    if chat_id in active_sessions and active_sessions[chat_id].get('is_running'):
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="🛑 Stop It", callback_data="cancel_scan"))
        builder.add(InlineKeyboardButton(text="▶️ Continue", callback_data="continue_scan"))
        
        await message.answer(
            "⚠️ WARNING: Engine is currently engaged.\n\n"
            "Would you like to continue the scanning process or else just stop it?", 
            reply_markup=builder.as_markup()
        )
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("Error: Target missing. Usage: /scan <target>")
        return
    
    target = args[1]
    
    # Kunci sesi untuk chat ini
    active_sessions[chat_id] = {'is_running': True, 'target': target}
    
    await message.answer(f"Target: {target}\nStatus: Initializing Phase 1 (Recon)...")
    
    # 2. FASE RECON (crt.sh / OTX)
    subdomains = fetch_subdomains(target)
    if not subdomains:
        subdomains = fetch_subdomains_otx(target)
        
    if not subdomains:
        await message.answer("Error: No subdomains found. Aborting.")
        active_sessions[chat_id]['is_running'] = False
        return

    await message.answer(f"Status: Probing {len(subdomains)} targets...")
    
    # 3. FASE PROBER
    probe_results = await probe_subdomains(subdomains)
    live_targets = probe_results.get('live', [])
    
    if not live_targets:
        await message.answer("Error: No live targets found. Aborting.")
        active_sessions[chat_id]['is_running'] = False
        return

    # 4. INTERACTIVE MENU (Milih Senjata)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="☢️ Nuclei", callback_data=f"attack_nuclei_{target}"))
    builder.add(InlineKeyboardButton(text="🗺️ NMap", callback_data=f"attack_nmap_{target}"))
    builder.add(InlineKeyboardButton(text="📂 Ffuf", callback_data=f"attack_ffuf_{target}"))
    builder.adjust(3) # Susun 3 tombol sebaris
    
    report_text = (
        f"RECON COMPLETE: {target}\n"
        f"------------------\n"
        f"Subdomains Found: {len(subdomains)}\n"
        f"Live Assets: {len(live_targets)}\n"
        f"------------------\n"
        f"Select attack engine for Phase 2:"
    )
    
    await message.answer(report_text, reply_markup=builder.as_markup())
    # Lepas lock sementera karena prober sudah selesai, nunggu user klik tombol
    active_sessions[chat_id]['is_running'] = False 

# Nangkep klik tombol
@dp.callback_query()
async def handle_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    data = callback_query.data
    
    await bot.answer_callback_query(callback_query.id)
    
    # Handle Cancel Request
    if data == "cancel_scan":
        active_sessions[chat_id] = {'is_running': False}
        await bot.send_message(chat_id, "Status: Scanning process terminated by user.")
        return
    elif data == "continue_scan":
        await bot.send_message(chat_id, "Status: Ignoring interruption. Engine is still running.")
        return
        
    # Handle Attack Engine Selection
    if data.startswith("attack_"):
        # Kunci lagi karena proses berat mau jalan
        active_sessions[chat_id] = {'is_running': True}
        
        _, engine, target = data.split('_')
        
        await bot.send_message(chat_id, f"Status: Initiating {engine.upper()} strike on {target}...\nPlease wait.")
        
        if engine == "nuclei":
            results = await run_nuclei(target)
            
            critical = sum(1 for item in results if item.get('info', {}).get('severity') == 'critical')
            high = sum(1 for item in results if item.get('info', {}).get('severity') == 'high')
            
            await bot.send_message(
                chat_id, 
                f"STRIKE COMPLETE: {target}\nEngine: NUCLEI\nFindings: {len(results)}\nCritical: {critical} | High: {high}"
            )
            
        elif engine == "nmap":
            await bot.send_message(chat_id, "Error: NMap engine not yet integrated.")
            
        elif engine == "ffuf":
            await bot.send_message(chat_id, "Error: Ffuf engine not yet integrated.")
            
        # Selesai attack, lepas kunci
        active_sessions[chat_id]['is_running'] = False

async def main():
    print("Bot is running 24/7. Press Ctrl+C to stop.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())