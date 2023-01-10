import time,os
import rbot_config as c
import rbot_driver as d

url = {
    'shaurya' :   'https://voice.google.com/u/0/messages?itemId=t.%2B16692526760',
}

def send_sms(msg):
    d.input(d.gdriver, c.xpath['gvoice_msg_in'], msg) # enter text message
    d.click(d.gdriver, c.xpath['gvoice_send'])
    time.sleep(1)

def send_snapshot():   
    d.click(d.gdriver, c.xpath['gvoice_img_btn'])
    time.sleep(2)
    os.system(os.getcwd()+'\\upload.exe') # upload snapshot.png
    time.sleep(3)
    d.click(d.gdriver, c.xpath['gvoice_send'])

def receive_sms():
    prev_msg = d.get_text(d.gdriver, c.xpath['gvoice_rd_msg']).split()[-1]
    new_msg = prev_msg

    while (prev_msg == new_msg):
        new_msg = d.get_text(d.gdriver, path).split()[-1] 

    return new_msg

def resolve_2FA():
    d.take_snapshot(d.gdriver, 'snapshot.png')
    send_snapshot()

    return receive_sms()