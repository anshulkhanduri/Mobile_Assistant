"""
chatbot_logic.py
Knowledge base and response logic for the Knowledge Assistant chatbot.
Topic: Mobile Applications & Smartphone Usage
"""

import re
from groq import Groq

# Initialize Groq client with the provided API key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# ─────────────────────────────────────────────
#  KNOWLEDGE BASE — keyword → response mapping
# ─────────────────────────────────────────────
KNOWLEDGE_BASE = {

    # ── Greetings & Introduction ──────────────────────────────────────
    "hello": "Hello! 👋 Welcome to the Knowledge Assistant. I'm here to help you with mobile apps, phone features, and troubleshooting. What would you like to know?",
    "hi": "Hi there! 😊 How can I assist you with your smartphone or mobile apps today?",
    "hey": "Hey! Great to see you here. Ask me anything about mobile applications or smartphone usage!",
    "good morning": "Good morning! ☀️ Ready to help you with all things mobile. What's your question?",
    "good afternoon": "Good afternoon! 🌤️ How can I assist you with your phone or apps today?",
    "good evening": "Good evening! 🌙 I'm here to help with any mobile or app-related questions.",
    "how are you": "I'm doing great, thank you for asking! 😊 I'm ready to help you with mobile apps and smartphone tips. What's on your mind?",
    "what is your name": "I'm the Knowledge Assistant — your go-to guide for everything about mobile applications and smartphones! 📱",
    "who are you": "I'm the Knowledge Assistant, a chatbot designed to help you understand mobile apps, phone features, settings, and troubleshooting. Ask me anything!",
    "what can you do": "I can help you with:\n• 📲 Installing, updating & uninstalling apps\n• 📱 Phone features (screenshot, brightness, wallpaper, etc.)\n• 🌐 Internet connectivity (WiFi, Bluetooth, mobile data)\n• 🔧 Troubleshooting (slow phone, battery issues, storage)\n• 🔒 Security & privacy tips\n\nJust ask your question!",
    "help": "Sure! I can answer questions about mobile apps, phone settings, connectivity, troubleshooting, and security. Try asking something like 'How do I install an app?' or 'Why is my phone slow?'",

    # ── About the Chatbot ─────────────────────────────────────────────
    "who made you": "I was created as a college project to help users learn about mobile applications and smartphone usage. 🎓",
    "what is this chatbot": "This is the Knowledge Assistant — a rule-based chatbot built with Python Flask. It answers questions about mobile apps and smartphone usage.",
    "how do you work": "I work by matching your question keywords to a built-in knowledge base. If I recognise your query, I give you a helpful response. It's a rule-based system — simple but effective! 😊",
    "are you a robot": "Yes, I am a chatbot — a computer program designed to have conversations. I don't have feelings, but I am very good at answering mobile-related questions! 🤖",
    "are you human": "No, I'm a chatbot! I'm a computer program, not a human. But I'm here to help you just like a human assistant would. 😊",
    "what technology are you built with": "I'm built with Python and the Flask web framework for the backend, and plain HTML, CSS, and JavaScript for the front end. 💻",

    # ── App Installation ──────────────────────────────────────────────
    "how to install an app": "To install an app:\n1. Open the Google Play Store (Android) or App Store (iPhone).\n2. Search for the app by name.\n3. Tap **Install** (Android) or **Get** (iPhone).\n4. Wait for the download to finish. 🎉",
    "how to install app": "To install an app:\n1. Open the Google Play Store (Android) or App Store (iPhone).\n2. Search for the app by name.\n3. Tap **Install** (Android) or **Get** (iPhone).\n4. Wait for the download to finish. 🎉",
    "how to download app": "Open your App Store or Play Store, search for the app, and tap Install/Get. The app will download and appear on your home screen. 📲",
    "play store": "The Google Play Store is Google's official app marketplace for Android devices. You can search, install, update, and manage all your apps from there.",
    "app store": "The App Store is Apple's official app marketplace for iPhones and iPads. You can download free or paid apps directly from there.",
    "how to install app from unknown source": "On Android, go to **Settings → Security → Install Unknown Apps**, then enable permission for your file manager or browser. ⚠️ Only install apps from sources you trust!",
    "cannot install app": "If you can't install an app, try:\n1. Check your internet connection.\n2. Make sure you have enough storage.\n3. Clear the Play Store/App Store cache.\n4. Restart your phone and try again.",

    # ── App Uninstallation ────────────────────────────────────────────
    "how to uninstall app": "To uninstall an app:\n• **Android**: Long-press the app icon → Tap *Uninstall*.\n• **iPhone**: Long-press the app → Tap *Remove App* → *Delete App*.\nYou can also go to **Settings → Apps** to remove it from there.",
    "how to delete app": "Long-press the app icon on your home screen and select **Uninstall** (Android) or **Remove App** (iPhone). This will delete the app and free up storage.",
    "how to remove app": "Go to **Settings → Apps & Notifications**, select the app, and tap **Uninstall**. Or long-press the app icon on the home screen and choose Uninstall.",

    # ── App Updates ───────────────────────────────────────────────────
    "how to update app": "To update an app:\n1. Open the Play Store or App Store.\n2. Tap your profile icon → *Manage Apps*.\n3. Find the app and tap **Update**, or tap **Update All**. 🔄",
    "how to auto update apps": "Enable auto-updates: Open Play Store → Profile → Settings → **Network Preferences → Auto-update apps**. On iPhone, go to **Settings → App Store → App Updates** and toggle it on.",
    "why update apps": "Updating apps gives you new features, bug fixes, performance improvements, and important security patches. Always keep your apps up to date! 🔒",
    "latest version of app": "To check the latest version, open the Play Store or App Store, search for the app, and view its details. If an **Update** button appears, a newer version is available.",

    # ── Phone Features — Screenshot ───────────────────────────────────
    "how to take screenshot": "To take a screenshot:\n• **Android**: Press **Power + Volume Down** simultaneously.\n• **Samsung**: Press **Power + Home** button.\n• **iPhone**: Press **Side Button + Volume Up** at the same time.\nYour screenshot will be saved in the Photos app! 📸",
    "screenshot": "A screenshot captures whatever is currently displayed on your screen. On most Android phones, press **Power + Volume Down** together. On iPhones, press the **Side + Volume Up** buttons.",
    "scrolling screenshot": "For a scrolling (long) screenshot, take a normal screenshot, then tap the **Scroll** or **Capture More** option that appears at the bottom. This feature is available on most Android phones.",

    # ── Phone Features — Brightness ───────────────────────────────────
    "how to adjust brightness": "Swipe down from the top of your screen to open the notification panel. Find the **brightness slider** and drag it left (dimmer) or right (brighter). 🔆",
    "brightness": "Adjust screen brightness by swiping down on your home screen to reveal the Quick Settings panel and using the brightness slider. You can also go to **Settings → Display → Brightness**.",
    "auto brightness": "Enable auto-brightness (adaptive brightness) in **Settings → Display → Adaptive Brightness**. Your phone will automatically adjust brightness based on your environment. 🌗",

    # ── Phone Features — Wallpaper ────────────────────────────────────
    "how to change wallpaper": "To change your wallpaper:\n1. Long-press an empty area on your home screen.\n2. Tap **Wallpapers**.\n3. Pick an image from your gallery or built-in wallpapers.\n4. Set it as home screen, lock screen, or both. 🖼️",
    "wallpaper": "You can set any image as your wallpaper! Go to **Settings → Display → Wallpaper** or long-press your home screen and select Wallpapers.",

    # ── Phone Features — Screen Recording ─────────────────────────────
    "how to record screen": "To record your screen:\n• **Android**: Swipe down to Quick Settings and tap **Screen Recorder**.\n• **iPhone**: Go to **Settings → Control Center**, add *Screen Recording*, then tap the record icon from the Control Center.\n🎥 The video is saved to your gallery.",
    "screen recording": "Screen recording captures everything happening on your screen as a video. Look for the Screen Recorder icon in your Quick Settings panel (swipe down twice to see all icons).",

    # ── Phone Features — Restart ──────────────────────────────────────
    "how to restart phone": "Press and hold the **Power button** for 2–3 seconds, then tap **Restart** from the menu that appears. Your phone will reboot. 🔄",
    "restart phone": "Hold the Power button and select **Restart**. Restarting your phone can fix many minor issues like freezing, slow performance, and app crashes.",
    "how to force restart phone": "If your phone is frozen:\n• **Android**: Hold **Power + Volume Down** for 10 seconds.\n• **iPhone (Face ID)**: Quickly press Volume Up, then Volume Down, then hold the Side button until it restarts.",

    # ── Phone Features — Volume & Sound ───────────────────────────────
    "how to adjust volume": "Use the **Volume Up / Volume Down** buttons on the side of your phone to adjust the volume. Or go to **Settings → Sound** to customize ringtone, media, and notification volumes.",
    "silent mode": "Press the Volume Down button until the phone goes silent, or toggle the mute switch. On Android, pressing Volume Down shows a notification options panel where you can select silent or vibrate.",

    # ── Internet — WiFi ───────────────────────────────────────────────
    "how to connect wifi": "To connect to WiFi:\n1. Go to **Settings → WiFi**.\n2. Toggle WiFi **On**.\n3. Select your network from the list.\n4. Enter the password and tap **Connect**. 📶",
    "wifi": "WiFi lets you connect to the internet via a wireless router. Enable it in **Settings → WiFi**, choose your network, and enter the password. WiFi is faster and saves mobile data.",
    "wifi not connecting": "If WiFi isn't working:\n1. Turn WiFi off and on again.\n2. Forget the network and reconnect.\n3. Restart your phone and the router.\n4. Check if the password is correct.\n5. Move closer to the router.",

    # ── Internet — Bluetooth ──────────────────────────────────────────
    "how to connect bluetooth": "To connect Bluetooth:\n1. Go to **Settings → Bluetooth** and toggle it **On**.\n2. Put the other device in pairing mode.\n3. Select the device from the available list.\n4. Accept the pairing request. 🔵",
    "bluetooth": "Bluetooth allows wireless connection between devices like headphones, speakers, and cars. Enable it in **Settings → Bluetooth** and pair with nearby devices.",
    "bluetooth not working": "Bluetooth troubleshooting:\n1. Turn Bluetooth off and on again.\n2. Unpair and re-pair the device.\n3. Restart both devices.\n4. Make sure the other device is in pairing mode and close enough (within ~10 metres).",

    # ── Internet — Mobile Data ─────────────────────────────────────────
    "how to turn on mobile data": "Go to **Settings → Network → Mobile Data** and toggle it on. Or swipe down to the Quick Settings panel and tap the **Mobile Data** icon. 📡",
    "mobile data": "Mobile data lets you access the internet using your cellular network (4G/5G). Enable it in Settings or from the Quick Settings panel when you're not near a WiFi connection.",
    "mobile data not working": "If mobile data isn't working:\n1. Toggle mobile data off and on.\n2. Check if you have remaining data balance.\n3. Go to **Settings → Network** and verify the APN settings.\n4. Restart your phone.",

    # ── Internet — Hotspot ─────────────────────────────────────────────
    "how to turn on hotspot": "To enable a mobile hotspot:\n1. Go to **Settings → Network → Hotspot & Tethering**.\n2. Tap **Mobile Hotspot** and turn it on.\n3. Set a name (SSID) and password.\n4. Other devices can now connect using that password. 🔥",
    "hotspot": "A mobile hotspot shares your phone's internet connection with other devices via WiFi. Be aware that it consumes battery and mobile data quickly.",

    # ── Internet — Airplane Mode ───────────────────────────────────────
    "airplane mode": "Airplane mode disables all wireless communications (WiFi, Bluetooth, cellular). Go to **Settings → Airplane Mode** or toggle it from the Quick Settings panel. It's still safe to use wifi/bluetooth manually after enabling airplane mode.",

    # ── Troubleshooting — Slow Phone ──────────────────────────────────
    "phone is slow": "If your phone is slow:\n1. Restart the phone.\n2. Close background apps.\n3. Clear app caches (**Settings → Apps → Select App → Clear Cache**).\n4. Free up storage space.\n5. Disable animations in Developer Options.\n6. Consider a factory reset if the issue persists.",
    "slow phone": "A slow phone is often caused by low storage, too many background apps, or outdated software. Try restarting, clearing cache, and deleting unused apps.",
    "why is my phone slow": "Your phone may be slow due to: low storage space, too many apps running in the background, old software, or malware. Regular maintenance (clearing cache, updating apps) helps a lot!",

    # ── Troubleshooting — Battery ──────────────────────────────────────
    "battery draining fast": "To improve battery life:\n1. Reduce screen brightness.\n2. Turn off WiFi, Bluetooth, GPS when not in use.\n3. Enable Battery Saver mode.\n4. Close background apps.\n5. Identify battery-hungry apps in **Settings → Battery**.",
    "how to save battery": "Save battery by: lowering brightness, using dark mode, turning off location services, disabling background app refresh, and enabling **Battery Saver** in Settings. 🔋",
    "battery not charging": "If your phone isn't charging:\n1. Check the charging cable for damage.\n2. Try a different charger or USB port.\n3. Clean the charging port carefully.\n4. Restart the phone.\n5. If nothing works, the battery may need replacement.",

    # ── Troubleshooting — Overheating ─────────────────────────────────
    "phone overheating": "If your phone is overheating:\n1. Remove the case for better ventilation.\n2. Avoid using intensive apps for long periods.\n3. Lower screen brightness.\n4. Avoid charging while using phone.\n5. Keep the phone away from direct sunlight. ☀️",
    "phone getting hot": "A warm phone is normal during gaming or charging. But if it's very hot:\n• Close heavy apps\n• Stop charging temporarily\n• Move to a cooler environment\n• Avoid direct sunlight",

    # ── Troubleshooting — Storage ──────────────────────────────────────
    "storage full": "To free up storage:\n1. Delete unused apps.\n2. Clear app caches (**Settings → Apps → Clear Cache**).\n3. Move photos to Google Photos or cloud storage.\n4. Delete downloaded files.\n5. Use a microSD card if your phone supports it. 💾",
    "how to free up storage": "You can free storage by:\n• Deleting old photos and videos\n• Removing apps you don't use\n• Clearing app caches\n• Moving data to cloud storage (Google Drive, iCloud)\n• Deleting downloaded files",
    "phone storage management": "Go to **Settings → Storage** to see a breakdown of what's using your space. You can manage apps, delete media files, and move data from there.",

    # ── Troubleshooting — App Crashes ─────────────────────────────────
    "app keeps crashing": "If an app keeps crashing:\n1. Force stop the app (**Settings → Apps → Force Stop**).\n2. Clear its cache and data.\n3. Update the app.\n4. Uninstall and reinstall the app.\n5. Restart your phone.",
    "app not opening": "Try force-stopping the app, clearing its cache, and reopening it. If it still won't open, uninstall and reinstall it from the Play Store or App Store.",
    "app freezing": "If an app freezes, press the Recent Apps button and swipe the app away to close it. Then reopen it. You can also go to **Settings → Apps** and force stop the app.",

    # ── Security & Privacy — Phone Lock ───────────────────────────────
    "how to lock phone": "Set up a screen lock:\n1. Go to **Settings → Security → Screen Lock**.\n2. Choose from PIN, password, pattern, fingerprint, or face recognition.\n3. Follow the setup steps.\n🔒 This protects your personal data.",
    "screen lock": "A screen lock prevents unauthorised access to your phone. Set it up via **Settings → Security → Screen Lock** using a PIN, password, pattern, or biometrics.",
    "how to set up fingerprint": "To add fingerprint unlock:\n1. Go to **Settings → Security → Fingerprint**.\n2. Follow the on-screen instructions to register your fingerprint.\n3. You can add multiple fingerprints. Your phone will unlock instantly when you place a registered finger on the sensor. 👆",
    "how to set up face recognition": "Go to **Settings → Security → Face Recognition** and follow the prompts to scan your face. Once set up, your phone will unlock just by looking at it! 😊",
    "forgot password": "If you forgot your phone PIN or password:\n• On Android: After several failed attempts, tap *Forgot PIN* and sign in with your Google account.\n• On iPhone: You'll need to restore via iTunes/Finder.\n⚠️ This may erase your data, so set up regular backups!",

    # ── Security & Privacy — Suspicious Apps ──────────────────────────
    "suspicious app": "If you find a suspicious app:\n1. Do not grant it unnecessary permissions.\n2. Go to **Settings → Apps**, find the app, and **Uninstall** it.\n3. Run a Play Protect scan (Play Store → Profile → Play Protect).\n4. Change your passwords as a precaution. 🛡️",
    "how to check app permissions": "Go to **Settings → Apps**, select an app, and tap **Permissions** to see what the app can access (camera, microphone, location, etc.). Revoke any permissions that seem unnecessary.",
    "how to protect phone from virus": "Protect your phone by:\n1. Only downloading apps from official stores.\n2. Keeping your OS and apps updated.\n3. Avoiding suspicious links.\n4. Using Google Play Protect.\n5. Not connecting to untrusted WiFi networks. 🔐",
    "privacy": "To enhance privacy:\n• Review app permissions regularly\n• Use a VPN on public WiFi\n• Enable two-factor authentication\n• Lock sensitive apps\n• Avoid sharing personal details on unknown websites",

    # ── Ending Conversation ───────────────────────────────────────────
    "thank you": "You're welcome! 😊 Feel free to come back anytime you have questions about mobile apps or your smartphone. Happy to help!",
    "thanks": "Glad I could help! 👍 Don't hesitate to ask if you have more questions.",
    "bye": "Goodbye! 👋 Take care and enjoy your smartphone experience. See you next time!",
    "goodbye": "Goodbye! 😊 Remember, I'm always here whenever you need mobile help. Stay safe!",
    "see you": "See you! 👋 Have a great day and don't hesitate to return if you have any mobile-related questions!",
    "exit": "Alright, take care! 😊 Come back whenever you need help with apps or your phone.",
}

MAIN_MENU_TEXT = """Welcome to the Mobile Application Knowledge Assistant!
Please select a topic by typing its number:
1. App Installation
2. Mobile Settings
3. Internet Connectivity
4. Basic Troubleshooting
0. Exit"""

APP_INSTALLATION_MENU = """App Installation Menu:
1. How to install an app
2. How to uninstall an app
3. How to update apps
9. Main Menu
0. Exit"""

MOBILE_SETTINGS_MENU = """Mobile Settings Menu:
1. Adjust Brightness
2. Change Wallpaper
3. Screen Lock & Security
9. Main Menu
0. Exit"""

INTERNET_MENU = """Internet Connectivity Menu:
1. Connect to WiFi
2. Connect Bluetooth
3. Mobile Data Issues
9. Main Menu
0. Exit"""

TROUBLESHOOTING_MENU = """Basic Troubleshooting Menu:
1. Phone is Slow
2. Battery Draining Fast
3. App Keeps Crashing
4. Storage Full
9. Main Menu
0. Exit"""

CONTINUE_PROMPT = "\n\nType 9 for Main Menu, or 0 to Exit."

def handle_unrecognized(user_input: str, current_menu: str, state: str) -> tuple[str, str]:
    if not user_input.isnumeric():
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are the Knowledge Assistant, an expert in mobile applications and smartphone usage. If the user's query is completely unrelated to mobile phones, apps, or smartphone technology, you must reply EXACTLY with the text 'OUT_OF_SCOPE' and nothing else. Otherwise, provide a concise, friendly, and helpful response."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                temperature=0.7,
                max_tokens=256,
            )
            groq_answer = completion.choices[0].message.content.strip()
            
            if "OUT_OF_SCOPE" in groq_answer:
                return ("I'm sorry, I can only provide assistance with mobile applications and smartphone usage. Let's start over!\n\n" + MAIN_MENU_TEXT, "MAIN_MENU")

            return (groq_answer + "\n\n---\n" + current_menu, state)
        except Exception as e:
            print(f"Groq API error: {e}")
            return ("Sorry, I didn't understand that. Please select a valid option.\n\n" + current_menu, state)
    
    return ("Invalid option. Please select a valid number from the menu.\n\n" + current_menu, state)


def get_response(user_input: str, state: str) -> tuple[str, str]:
    text = user_input.lower().strip()

    # Global navigation commands
    if text in ["0", "exit", "quit", "bye"]:
        return ("Goodbye! Have a great day! 👋\n(Type anything to start over)", "EXIT")
    
    if state == "EXIT":
        return (MAIN_MENU_TEXT, "MAIN_MENU")

    if text in ["9", "main menu"]:
        return (MAIN_MENU_TEXT, "MAIN_MENU")
    
    # State machine logic
    if state == "MAIN_MENU":
        if text == "1":
            return (APP_INSTALLATION_MENU, "APP_INSTALLATION")
        elif text == "2":
            return (MOBILE_SETTINGS_MENU, "MOBILE_SETTINGS")
        elif text == "3":
            return (INTERNET_MENU, "INTERNET")
        elif text == "4":
            return (TROUBLESHOOTING_MENU, "TROUBLESHOOTING")
        else:
            if text in ["hello", "hi", "hey"]:
                return (MAIN_MENU_TEXT, "MAIN_MENU")
            return handle_unrecognized(text, MAIN_MENU_TEXT, state)
            
    elif state == "APP_INSTALLATION":
        if text == "1":
            return (KNOWLEDGE_BASE["how to install an app"] + CONTINUE_PROMPT, "APP_INSTALLATION")
        elif text == "2":
            return (KNOWLEDGE_BASE["how to uninstall app"] + CONTINUE_PROMPT, "APP_INSTALLATION")
        elif text == "3":
            return (KNOWLEDGE_BASE["how to update app"] + CONTINUE_PROMPT, "APP_INSTALLATION")
        else:
            return handle_unrecognized(text, APP_INSTALLATION_MENU, state)

    elif state == "MOBILE_SETTINGS":
        if text == "1":
            return (KNOWLEDGE_BASE["how to adjust brightness"] + CONTINUE_PROMPT, "MOBILE_SETTINGS")
        elif text == "2":
            return (KNOWLEDGE_BASE["how to change wallpaper"] + CONTINUE_PROMPT, "MOBILE_SETTINGS")
        elif text == "3":
            return (KNOWLEDGE_BASE["how to lock phone"] + CONTINUE_PROMPT, "MOBILE_SETTINGS")
        else:
            return handle_unrecognized(text, MOBILE_SETTINGS_MENU, state)

    elif state == "INTERNET":
        if text == "1":
            return (KNOWLEDGE_BASE["how to connect wifi"] + CONTINUE_PROMPT, "INTERNET")
        elif text == "2":
            return (KNOWLEDGE_BASE["how to connect bluetooth"] + CONTINUE_PROMPT, "INTERNET")
        elif text == "3":
            return (KNOWLEDGE_BASE["mobile data not working"] + CONTINUE_PROMPT, "INTERNET")
        else:
            return handle_unrecognized(text, INTERNET_MENU, state)
            
    elif state == "TROUBLESHOOTING":
        if text == "1":
            return (KNOWLEDGE_BASE["phone is slow"] + CONTINUE_PROMPT, "TROUBLESHOOTING")
        elif text == "2":
            return (KNOWLEDGE_BASE["battery draining fast"] + CONTINUE_PROMPT, "TROUBLESHOOTING")
        elif text == "3":
            return (KNOWLEDGE_BASE["app keeps crashing"] + CONTINUE_PROMPT, "TROUBLESHOOTING")
        elif text == "4":
            return (KNOWLEDGE_BASE["storage full"] + CONTINUE_PROMPT, "TROUBLESHOOTING")
        else:
            return handle_unrecognized(text, TROUBLESHOOTING_MENU, state)

    else:
        return (MAIN_MENU_TEXT, "MAIN_MENU")
