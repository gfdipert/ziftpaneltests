import sys
from assets_check_sel import LinkTests

if sys.platform == 'win32':
    import win_unicode_console
    win_unicode_console.enable() 
    #needed for windows because windows is stupid

tenquens = LinkTests("http://demos.ziftsolutions.com/sample/InnovativeTechnology/?a=qlik&wid=ff808181569b6fc10156a08e41a334b7&zPage=resources-d1ef094d")
tenquens.WhitePaper()