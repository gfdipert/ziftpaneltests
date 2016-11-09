from splinter import Browser
import sys

if sys.platform == 'win32':
    import win_unicode_console
    win_unicode_console.enable() 
    #needed for windows because windows is stupid

with Browser('chrome') as browser:
    url = "http://demos.ziftsolutions.com/sample/InnovativeTechnology/?a=qlik&wid=ff808181569b6fc10156a08e41a334b7&zPage=resources-d1ef094d"
    browser.visit(url)
 
    g_links = '?zPage='
    wp_links_found = browser.find_link_by_partial_text('White Paper: ')
 
    for link in wp_links_found:
        if 'target="_blank"' in link.outer_html and g_links not in link.outer_html:
            title = link.text[13:]
            try:
                link.click()
                if browser.is_text_present(title):
                    docstatus = link.text + " is linking to the correct document."
                else:
                    docstatus = link.text + " is not linking to the correct document."
                print docstatus
            except:
                print "Oops, I failed with " + link.text
        if g_links in link.outer_html:
            docstatus = link.text + " is gated."
            print docstatus
        if 'target="_blank"' not in link.outer_html and g_links not in link.outer_html:
            title = link.text[13:]
            try:
                link.click()
                if browser.is_text_present(title):
                    docstatus = link.text + " is linking to the correct document, but needs to open in a new tab."
                    browser.back()
                else:
                    docstatus = link.text + " is not linking to the correct document, and needs to open in a new tab."
                print docstatus
            except:
                print "Oops, I failed with " + link.text
