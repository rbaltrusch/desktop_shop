# desktop_shop
Desktop mock shop application interfacing with a generated database of customers, products and transactions (Python / SQLite3).

Considerations/Limitations/Problems:

	no cache: shopping cart gets discarded when session is disconnected
	no networking/server (to reduce extra complexity)

A few screenshots of the application:

![Screenshot of the application GUI](desktop_shop/gui/media/screenshot_new1.png?raw=true "Screenshot of the application GUI")
*Screenshot of the home view in the application GUI*

![Screenshot of the application GUI](desktop_shop/gui/media/screenshot_new2.png?raw=true "Screenshot of the application GUI")
*Screenshot of the register view in the application GUI*

![Screenshot of the application GUI](desktop_shop/gui/media/screenshot_new3.png?raw=true "Screenshot of the application GUI")
*Screenshot of the login view in the application GUI*

![Screenshot of the application GUI](desktop_shop/gui/media/screenshot_new4.png?raw=true "Screenshot of the application GUI")
*Screenshot of the profile view in the application GUI*

![Screenshot of the application GUI](desktop_shop/gui/media/screenshot_new5.png?raw=true "Screenshot of the application GUI")
*Screenshot of the checkout view in the application GUI*

To try out the graphical database application, simply install all the required packages (specified in requirements.txt) and run gui.py.

Written in Python 3.8.3
