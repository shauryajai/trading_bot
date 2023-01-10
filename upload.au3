#include <AutoItConstants.au3>

MouseClick($MOUSE_CLICK_LEFT, 570, 244, 1)
MouseClick($MOUSE_CLICK_LEFT, 680, 537, 1)
Sleep(1000)
ControlFocus("Open","","Edit1")
ControlSetText("Open","","Edit1","E:\robinhood_bot\rbot_v4\snapshot.png")
ControlClick("Open","","Button1")
Sleep(3000)
MouseClick($MOUSE_CLICK_LEFT, 310, 658, 1)
