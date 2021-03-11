import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
#init
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
#splash screen
disp.clear()
disp.display()
image = Image.open('/home/pi/senior_design/finalizing/orange_oled_32.ppm').convert('1')
disp.image(image)
disp.display()
time.sleep(1)
#show ip
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = 0
top = 8
bottom = 14
x = 25
font = ImageFont.load_default()
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('/home/pi/senior_design/finalizing/The Impostor.ttf', 12)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((x, top),"WELCOME!",  font=font, fill=255)
disp.image(image)
disp.display()
time.sleep(1)

font = ImageFont.truetype('/home/pi/senior_design/finalizing/pixelmix.ttf', 8)
draw.rectangle((0,0,width,height), outline=0, fill=0)
disp.clear()
disp.display()

cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell = True )
cmd = "whoami | cut -d\' \' -f1"
uname = subprocess.check_output(cmd, shell = True )
cmd = "hostname | cut -d\' \' -f1"
hostnm = subprocess.check_output(cmd, shell = True)
#print(IP)
#print(uname)

draw.text((6, 0),       'host: ' + str(hostnm, 'utf-8') + 'user: ' + str(uname,'utf-8') + 'addr: ' + str(IP,'utf-8').strip('\n') + ' ',  font=font, fill=255)
disp.image(image)
disp.display()
