This is a code of web server for md5 hash calculating by url.

Start guide:

1. Download project files
On project page (https://github.com/elqver/bg_test) push button "Clone or download" -> Download ZIP 
Unzip it with your favorite tool

2. Sure that you have Python3 (https://www.python.org/downloads/)
And pip, virtualenv (https://gist.github.com/frfahim/73c0fad6350332cef7a653bcd762f08d)

3. Install packages from requirements.txt (! be sure virtual enviroment was activated for avoiding collisions)
pip install -r requirements.txt 

4. Put your gmail address and password in emailconfig.py

5. Change secure apps setting in your google account (https://myaccount.google.com/lesssecureapps)

6. Put desired socket into SERVER_NAME variable in server_config.py

7. Run main.py
python main.py
