# prayer-time-iot

<h1>Notes: Make sure that all below steps are done</h1>

1- The following folders must be existed in the project (Starting from root path)

```
sounds
sounds/azan
sounds/quran
sounds/ramadan
sounds/ramadan/sounds
sounds/ramadan/voices
sounds/ramadan/voices/0_min
sounds/ramadan/voices/10_min
sounds/ramadan/voices/20_min
```

2- All sounds must have '.mp3 extension'

3- azan sounds must be existed and named as following:

```
azan_NUMBER.mp3
```

<i>NOTE: NUMBER can start from 1 example: azan_1.mp3, azan_2.mp3, azan_3.mp3, ...</i>

4- quran sounds must be existed and named as following:

```
quran_NUMBER.mp3
```

<i>NOTE: NUMBER can start from 1 example: quran_1.mp3, quran_2.mp3, quran_3.mp3, ... </i>

5- imsak sounds existed in <strong>ramadan/sounds</strong> must be existed as following:

```
sound_NUMBER.mp3
```

<i>NOTE: NUMBER can start from 1 example: sound_1.mp3, sound_2.mp3, sound_3.mp3, ...</i>

6- voice before 22 minutes from imsak must be existed in <strong>ramadan/voices/before_imsak/20_min</strong> as following:

```
voice_NUMBER.mp3
```

<i>NOTE: NUMBER can start from 1 example: voice_1.mp3, voice_2.mp3, voice_3.mp3, ...</i>

7- voice before 10 minutes from imsak must be existed in <strong>ramadan/voices/before_imsak/10_min</strong> as following:

```
voice.mp3
```

8- voice at imsak must be existed in <strong>ramadan/voices/before_imsak/0_min</strong> as following:

```
voice.mp3
```

9- <strong>For the LCD </strong> You must follow instructions for the LCD I2C by visiting **[the-raspberry-pi-guy](https://github.com/the-raspberry-pi-guy/lcd)**

10- Change the name of <strong>.env.example</strong> to <strong>.env</strong> and implement the appropriate values.

<strong><i>Note: All ranged files (e.g. azan, quran, imsak sounds and 22 min before imsak sounds) <u>MUST NOT HAVE A MISSED NUMBER BETWEEN THE RANGE</u>. Example about imsak sounds:</i></strong>

<strong> ✅ Correct: All files are named from 1 to 3</strong>

```
sound_1.mp3, sound_2.mp3, sound_3.mp3, ...
```

<strong> ❌ Wrong: sound_2.mp3 name is missed</strong>

```
sound_1.mp3, sound_3.mp3, sound_4.mp3, ...
```

<h1>Running main python file</h1>
1- Create virtual environment:

```
python -m venv myenv
```

2- Activate virtual environment:

```
source myenv/bin/activate
```

3- Download packages for playing sounds and dotenv

```
pip install RPi.GPIO python-vlc pydub python-dotenv smbus
```

4- Run main python file (Make sure that the terminal is navigated to the project's root path)

```
python main.py
```
