#from collections import deque

xpath = {
    'stk_val_xpath' :   '//*[@id="sdp-market-price"]/h2/span/span/div/div[1]',
    'stk_buy_power' :   '//*[@id="sdp-ticker-symbol-highlight"]/aside/div[1]/form/footer/div/span/div',
    'cpt_buy_power' :   '//*[@id="react_root"]/main/div[2]/div/div/div/div/div/div/div[2]/div/form/div/footer',
    'buying_power'  :   '//*[@id="react_root"]/main/div[3]/div/div/div/div/div/div/div[2]/div/form/div/footer/div',
    'selling power' :   '//*[@id="sdp-ticker-symbol-highlight"]/aside/div[1]/form/footer/div',
    'buy_tab'       :   '//*[@id="sdp-ticker-symbol-highlight"]/aside/div[1]/form/div[1]/div/div[1]/div/div/div[1]/div/div/h3/span/span',
    'sell_tab'      :   '//*[@id="sdp-ticker-symbol-highlight"]/aside/div[1]/form/div[1]/div/div[1]/div/div/div[2]/div/div/h3/span/span',
    'buy_input'     :   '//*[@id="sdp-ticker-symbol-highlight"]/aside/div[1]/form/div[2]/div/div[3]/div/div/div',
    'review_order'  :   '//*[@id="sdp-ticker-symbol-highlight"]/aside/div[1]/form/div[3]/div/div[2]/div[1]/div/button',
    'order_done'    :   '//*[@id="sdp-ticker-symbol-highlight"]/aside/div[1]/div/div[3]/div[1]/button',
    'units_traded'  :   '//*[@id="sdp-ticker-symbol-highlight"]/aside/div[1]/div/div[1]/div[2]/div',
    'buy_in_drp_dwn':   '//*[@id="sdp-ticker-symbol-highlight"]/aside/div[1]/form/div[2]/div/div[2]/div/div/div/div/div/button',
    'buy_in_usd'    :   '//*[@id="downshift-##-item-1"]',
    'sell_in_usd'   :   '//*[@id="downshift-2-item-1"]/div/span',
    'login_id'      :   '//*[@id="react_root"]/div[1]/div[2]/div/div/div/div/div/form/div/div[1]/label/div[2]/input',
    'login_pass'    :   '//*[@id="current-password"]',
    'login_remember':   '//*[@id="react_root"]/div[1]/div[2]/div/div/div/div/div/form/div/div[3]/label/div/div/div',
    'login_remem_2' :   '//*[@id="react_root"]/div[3]/div/div[3]/div/div/section/div/div/form/div/div[3]/label/div/div/div',
    'login_submit'  :   '//*[@id="submitbutton"]/div/button/span/span/span',
    'login_continue':   '//*[@id="submitbutton"]/div/button',
    'duo_code_xpath':   '//*[@id="react_root"]/div[3]/div[2]/div[3]/div/div/section/div/div/form/div/div/input',
    'login_duo_cont':   '//*[@id="react_root"]/div[3]/div[2]/div[3]/div/div/section/div/footer/div[1]/button/span/span/span',
    'gvoice_msg_in' :   '//*[@id="messaging-view"]/div/md-content/gv-thread-details/div/div[2]/gv-message-entry/div/div[2]/md-input-container',
    'gvoice_send'   :   '//*[@id="ib2"]',
    'gvoice_img_btn':   '//*[@id="ib1"]',
    'gvoice_upld'   :   '//*[@id=":7"]/div',
    'gvoice_ul_win' :   '//*[@id="doclist"]/div/div[4]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[3]/div[1]/div',
    'gvoice_rd_msg' :   '//*[@id="messaging-view"]/div/md-content/gv-thread-details/div/gv-thread-item-list/div/gv-text-message-list/section/div/ul',
}

stk_type    = ''
stk_name    = ''
url         = 'https://robinhood.com/'
runtime                 = 0
available_cash          = float(0)  # Available Buying Power 
current_price           = float(0)  # current price of the security
#stock_volume            = 0         # current price of the security
buying_power            = float(0)  # total amount in dollars to be spent
trade_value             = float(0)  # per transaction limit of the stock
window                  = []#deque()   # sliding window
average_price           = float(0)
stock_trend             = 'Hold'  # rising, falling or steady trend
stop_loss               = float(0)  # stop loss value
stop_on                 = float(0)
pc                      = float(0)
pc_max                  = float(0)  # percent change max between consecutive windows
sl_max                  = float(0)  # trailing stop loss max
total_units             = float(0)
units_traded            = float(0)
actual_traded_units     = float(0)
trade_complete          = False
total_value             = float(0)
total_invested          = float(0)
profit                  = float(0)
profit_percent          = float(0)
interval                = 0
interval_timer_expired  = False
interval_timer          = 1
enable_trade            = True
heartbeat               = 0
dummy_trade             = True

# def static_vars(**kwargs):
    # def decorate(func):
        # for k in kwargs:
            # setattr(func, k, kwargs[k])
        # return func
    # return decorate

# Example to use static variables inside a function:
# @rbot.static_vars(x=0, y=0)
# def foo():
#   foo.x = 1
#   foo.y = 1
# here x and y will behave as static variables