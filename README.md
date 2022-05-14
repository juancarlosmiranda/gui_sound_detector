# README

I made this software to detect jokes sent by friends in WhatsApp groups.
Sometimes people would send WhatsApp audios to joke around, like moans for example.
This app tries to classify moan sounds using the hmm algorithm, but the framework could be useful for other tasks.
The sound dataset used here was created from Whatsapp audios collected from groups, I believe these are public.

![screen_1](https://github.com/juancarlosmiranda/gui_sound_detector/blob/master/img/screen_1.png?raw=true)




## Clone repo
```
git clone https://github.com/juancarlosmiranda/gui_sound_detector.git
```

## Requirements
* ffmpeg command -> Used to wav conversion '/usr/bin/ffmpeg'


## 1. Ubuntu package
```
sudo apt-get install python3-tk
sudo apt-get install ffmpeg
```

## 2. Install environment.
```
python3 -m pip install python-venv
pip3 install python-venv
python3 -m venv ./venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements_linux.txt
```


## 3. Configure settings
```
In ./conf/ui_recognition_settings.conf
Configure path to databases for test and training.
```

Launch with:
```
python UI_main_recognition.py
```

## Authorship
.

## Citation
If you find this code useful, please consider citing:
[gui_sound_extractor](https://github.com/juancarlosmiranda/gui_sound_detector/).