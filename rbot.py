import time, sys, traceback
import rbot_config as c
import rbot_gvoice as g
import rbot_driver as d
#import csv, os, pandas as pd, db_connect as db

def login():
    if 'Log In' in d.get_title(d.rdriver):
        g.send_sms('RBOT: Username')
        d.input(d.rdriver, c.xpath['login_id'], g.receive_sms())
        
        g.send_sms('RBOT: Password')
        d.input(d.rdriver, c.xpath['login_pass'], g.receive_sms())
        
        try:
            d.click(d.rdriver, c.xpath['login_remember'])
        except:
            pass

        d.click(d.rdriver, c.xpath['login_submit'])

    time.sleep(5)
    
    # Still not logged in? Must be 2FA <send sms via google voice to solve the puzzle>
    if 'Log In' in d.get_title(d.rdriver):
        result = g.resolve_2FA()
        print (" "*115, end = '\r')
        
        if result == 'Done':
            print (f'Logged in')
        else:
            print (f'Captcha code = {result}')
            # initiate captcha loading process

def verify_account():
    g.send_sms('RBOT: Password')
    d.input(d.rdriver, c.xpath['login_pass'], g.receive_sms())

    try:
        d.click(d.rdriver, c.xpath['login_remem_2'])
    except:
        pass

    d.click(d.rdriver, c.xpath['login_continue'])

    while 1:
        try:
            # we should see element for units traded if verification completes
            # if not, there'll be an exception
            # catch the exception and perform 2FA
            get_available_cash()
            break
        except:
            print (" "*115, end = '\r')
            result = g.resolve_2FA()
            
            if result == 'Done':
                print (f'Logged in')
            else:
                print (f'Duo code = {result}')
                d.input(d.rdriver, c.xpath['duo_code_xpath'], result)
                d.click(d.rdriver, c.xpath['login_duo_cont'])

def resolve_issue():
    result = g.resolve_2FA()
    print (" "*115, end = '\r')
    print (f'Result = {result}')

def get_available_cash():
    if c.stk_type == "stocks":
        str = d.get_text(d.rdriver, c.xpath['stk_buy_power'])
        c.available_cash = float(str[1:].split(" ")[0].replace(',',''))
    elif c.stk_type == "crypto":
        str = d.get_text(d.rdriver, c.xpath['cpt_buy_power'])
        c.available_cash = float(str.split()[0][1:].replace(',',''))

def get_stock_price():
    x = 1
    while x:
        val = d.get_text(d.rdriver, c.xpath['stk_val_xpath'])[1:]
        # volume = c.get_text(c.xpath['stk_volume_xpath'])[1:]
        if len(val):
            c.current_price = float(val)
            # c.stock_volume = volume
            x = 0

def execute_interval_timer():
    time.sleep(1)
    c.interval_timer_expired = False

    if c.interval_timer == c.interval:
        c.interval_timer_expired = True
        c.interval_timer = 1
    else:
        c.interval_timer += 1    

def add_to_window():
    c.window.append(c.current_price)

def compute_average():
    c.average_price = sum(c.window)/len(c.window)

def window_popall():
    for _i in range(len(c.window)):
        c.window.pop(0) #c.window.popleft() 

def remove_outliers():
    c.window.sort()
    c.window.pop(len(c.window)-1) # c.window.pop()
    c.window.pop(0) # #c.window.popleft()
    compute_average()

def set_stop(stop_on, stop_loss):
    c.stop_on = stop_on
    c.stop_loss = stop_loss

def execute_trade(amount):
    d.click(d.rdriver, c.xpath['buy_in_drp_dwn'])
    time.sleep(1)
    
    # try:
        # d.click(d.rdriver, c.xpath['buy_in_usd'])
    # except:
        # d.click(d.rdriver, c.xpath['sell_in_usd'])
    attempts = 1
    while attempts < 7:
        try:
            d.click(d.rdriver,  c.xpath['buy_in_usd'].replace('##',str(attempts)))
            break
        except:
            pass
        attempts += 1
    time.sleep(1)

    d.input(d.rdriver, c.xpath['buy_input'], amount)
    time.sleep(1)

    attempts = 0
    while attempts < 7: # limit the number of attempts
        attempts += 1

        try:
            d.click(d.rdriver, c.xpath['review_order'])
            time.sleep(1)
        except:
            break

    if attempts >= 7:
        resolve_issue()

    if 'History' in d.get_title(d.rdriver):
        d.rhood_open(c.url)

    elif 'Log In' in d.get_title(d.rdriver):
        verify_account()
        # If account verified on time, set trade complete to true. Else trade complete false
        # Complete the trade manually if it's not verified on time
        c.trade_complete = True

    else:
        try:
            c.actual_traded_units = d.get_text(d.rdriver, c.xpath['units_traded'])
            d.click(d.rdriver, c.xpath['order_done'])
            time.sleep(1)
        except:
            resolve_issue()

        c.trade_complete = True

def buy(amount):
    if c.enable_trade:
        d.click(d.rdriver, c.xpath['buy_tab'])
        time.sleep(1)

        if c.dummy_trade:
            c.trade_complete = True
        else:
            execute_trade(amount)

    if c.trade_complete:
        c.units_traded = amount/c.current_price
        c.total_units += c.units_traded
        c.buying_power -= amount

def sell(amount):
    if c.enable_trade:
        d.click(d.rdriver, c.xpath['sell_tab'])
        time.sleep(1)

        if c.dummy_trade:
            c.trade_complete = True
        else:
            execute_trade(amount)

    if c.trade_complete:
        c.units_traded = amount/c.current_price
        c.total_units -= c.units_traded
        c.buying_power += amount

def trade_stock():
    c.trade_complete = False

    if c.stock_trend == 'Rise':
        so = c.average_price
        sl = so*(100 - c.sl_max)/100
        set_stop(so, sl)

        if c.buying_power >= c.trade_value:
            buy(c.trade_value)
        elif c.buying_power >= 1:
            buy(c.buying_power)
        else:
            pass

    elif c.stock_trend == 'Fall':
        so = c.average_price
        sl = so
        set_stop(so, sl)
        
        current_value = c.total_units * c.current_price
        if current_value >= 1:
            sell(current_value)
        else:
            pass

    else: # stock_trend == 'Hold'
        c.units_traded = 0
        # pass

    c.total_value = c.total_units * c.current_price
    
    return 0

def percent_change():
    c.pc =  100 * (c.average_price - c.stop_on)/c.stop_on

def compute_trend():
    if c.pc >= c.pc_max: 
        c.stock_trend = 'Rise'

    elif c.average_price < c.stop_loss:
        c.stock_trend = 'Fall'

    else:
        c.stock_trend = 'Hold'

def print_erasable_status():
    print (" "*115, end = '\r')
    dp  = '.6f'
    sp = format(c.current_price,dp)
    avg = format(c.average_price,dp)
    so = format(c.stop_on,dp)
    sl = format(c.stop_loss,dp)
    print(f"Interval timer = {c.interval_timer}, Samples = {len(c.window)}, Stock Price = {sp}, Average = {avg}, so = {so}, sl = {sl}", end = '\r')

def print_trade_status():
    dp  = '.6f'
    dp2 = '.5f'

    sp = format(c.current_price,dp)
    avg = format(c.average_price,dp)
    pc = format(c.pc,dp)
    
    if c.pc < 0:
        pc = format(c.pc,dp2)
        
    td = c.stock_trend
    so = format(c.stop_on,dp)
    sl = format(c.stop_loss,dp)
    bp = format(c.buying_power,dp)
    tv = format(c.total_value,dp)
    gain = format(c.profit,dp)
    
    if c.profit < 0:
        gain = format(c.profit,dp2)
    
    msg = f'sp = {sp}, avg = {avg}, pc = {pc}, td = {td}, so = {so}, sl = {sl}, bp = {bp}, value = {tv}, gain = {gain}'
    print (msg)

    msg  = f'RBOT: {c.stk_name}, ' + msg
    msg += f', Units Traded {c.units_traded} (computed) {c.actual_traded_units} (actual)'
    g.send_sms(msg)

def calculate_profit():
    c.profit = (c.buying_power + c.total_value) - c.total_invested

def trade():
    remove_outliers()
    percent_change()
    compute_trend()
    trade_stock()
    calculate_profit()
    if c.trade_complete:
        print_trade_status()    

def rbot_init():
    c.stk_type       = "stocks" # stocks, crypto
    c.stk_name       = "SPY" # DOGE, SPY
    c.url            = c.url + c.stk_type + "/" + c.stk_name
    c.runtime        = 60*60*24*7*52
    c.buying_power   = 50
    c.trade_value    = 2
    c.interval       = 60*5#60*2
    c.pc_max         = 0.4
    c.sl_max         = 0.2
    c.total_invested = c.buying_power
    c.max_samples    = 10#30

    d.rhood_open(c.url)
    # d.rdriver.maximize_window()
    # d.rdriver.switch_to.window(d.rdriver.current_window_handle)
    time.sleep(5)
    get_available_cash()

    if c.trade_value > c.buying_power:
        print(f"ERROR: Trade_value ({c.trade_value}) cannot be greater than buying power ({c.buying_power})")
        return 0
    
    if c.buying_power > c.available_cash:
        print(f"ERROR: Buying power ({c.buying_power}) cannot be greater than available cash ({c.available_cash})")
        return 0

    get_stock_price()
    set_stop(c.current_price, c.current_price)
    add_to_window()
    compute_average()

    print(f"_"*110)
    print(f"Init Price = {c.current_price}, Available Cash = {c.available_cash}, Buying Power = {c.buying_power}, Trade value = {c.trade_value}")
    print(f"Runtime = {c.runtime}, Maximum Samples = {c.max_samples}, Wait Interval = {c.interval}")
    print(f"Percent Change Th = {c.pc_max}, Stop Loss Percent Th = {c.sl_max}, Stop On = {c.stop_on}, Stop Loss = {c.stop_loss}")
    print(f"_"*110)

    g.send_sms(f'Heartbeat {c.heartbeat} (OK)')

def main():
    start_time = time.time()
    time_taken = 0
    rbot_init()

    while time_taken < c.runtime:
        execute_interval_timer()

        try:
            get_stock_price()
        except:
            resolve_issue()
            get_stock_price()

        if c.interval_timer_expired:
            add_to_window()
            compute_average()

        if len(c.window) == c.max_samples:
            c.heartbeat += 1
            g.send_sms(f'Heartbeat {c.heartbeat} (OK)')
            trade()
            window_popall()

        print_erasable_status()
        time_taken  = time.time() - start_time

    print (" "*115, end = '\r')
    print("Time taken = ", time_taken)      

def run():
    try:
        d.rhood_open(c.url+'login')
        d.gvoice_open(g.url['shaurya'])
        login()
        main()

    except IndexError:
        print('== Exception Caught ==')
        exc_value= sys.exc_info()
        msg = 'Exception: ' + repr(traceback.format_exception(exc_value))
        print(msg)
        s.send_sms(msg)

    # except Exception as e:
        # #traceback.print_exc()
        # print(f'Exception: {e}')
        # s.send_sms(f'Exception: {e}')

    time.sleep(5)
    d.driver_close()

if __name__ == "__main__":
    run()