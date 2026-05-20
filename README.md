# AI-Trading-BOT
Step	Action Required
1. Server Hosting	Run trading_server.py on a cloud platform (e.g., AWS EC2, DigitalOcean Droplet) so it runs 24/7. Do not run this on your personal laptop, as the AI will die when your laptop goes to sleep.
2. Android Setup	Download Android Studio. Create a new "Empty Compose Activity" project. Paste the Kotlin code into MainActivity.kt.
3. Permissions	Open AndroidManifest.xml in Android Studio and add <uses-permission android:name="android.permission.INTERNET" /> above the <application> tag.
4. Network Config	In the Kotlin code, change SERVER_URL from 10.0.2.2 (Emulator localhost) to the public IP address of your AWS/DigitalOcean server.
5. Build & Install	Connect your Android phone via USB, enable Developer Mode, and click "Run" in Android Studio to install the APK directly to your device.