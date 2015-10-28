from zshtwt import User, api_zshtwt
from zshtwt import graphical
api_zshtwt.refresh()
window = graphical.Window()
window.fetch_screen(api_zshtwt.compare())
