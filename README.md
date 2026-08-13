# AI Chatbot

Free Gemini API se chalne wala chatbot. Do versions hai — terminal aur website.

## Setup (ek baar karna hai)

1. Yaha se free API key le lo (card nahi chahiye): https://aistudio.google.com/apikey
2. Is folder me terminal khol ke ye chalao:
   ```
   pip install -r requirements.txt
   ```

## Terminal wala chalane ke liye

```
python chatbot.py
```
Pehli baar chalate waqt API key maangega, paste kar do.

## Website wala chalane ke liye

```
python app.py
```
Fir browser me kholo: http://localhost:5000

Website me "Clear chat" button hai memory reset karne ke liye.

## Same WiFi pe doosron ke saath share karna

Tumhara laptop aur doosra device (phone/laptop) same WiFi pe hone chahiye.

1. `python app.py` chalao (ye already chal raha hai to Ctrl+C se band karke dobara chalao — naya code hai)
2. Apna computer ka local IP pata karo — CMD me:
   ```
   ipconfig
   ```
   "IPv4 Address" wali line dekho, kuch aisi dikhegi: `192.168.1.5`
3. Doosre device ke browser me type karo:
   ```
   http://192.168.1.5:5000
   ```
   (apna wala IP daalna, upar sirf example hai)

Agar nahi khulta:
- Windows Firewall ka popup aaya ho to "Allow" dabao
- Dono device same WiFi pe hone chahiye (mobile data/hotspot alag network hai)

## Internet pe LIVE karna (koi bhi, kahin se bhi access kare)

Free me Render.com use karenge. Card nahi chahiye.

1. **GitHub pe daalo:** Is poore folder ka GitHub repo bana lo (github.com pe free account, phir "New repository" → is folder ke files upload kar do).
2. **Render pe account banao:** https://render.com pe jaake GitHub se sign up karo.
3. **New Web Service:** Dashboard me "New +" → "Web Service" → apna GitHub repo select karo.
4. **Settings fill karo:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app` (Procfile already isko handle karta hai)
5. **API key daalo:** "Environment" tab me ek variable add karo:
   - Key: `GEMINI_API_KEY`
   - Value: apni key paste karo
6. **Deploy** dabao. 2-3 minute me ek live link milega jaise `https://tumhara-app.onrender.com` — ye link kisi ko bhi bhej sakte ho, kahin se bhi khulega.

Free plan pe agar 15 min tak koi use na kare to app so jaata hai — agli baar khulne me 30-40 second lag sakte hain, phir normal speed.

## Note

API key ek baar environment variable set kar doge to baar baar nahi maangega:
- Windows: `setx GEMINI_API_KEY "your-key-here"` (fir naya terminal kholna hoga)

Agar tumne apni API key kisi screenshot ya chat me paste kar di thi, wo regenerate kar lo yaha se: https://aistudio.google.com/apikey (purani delete, nayi bana lo — bas 10 second ka kaam hai).
