import sys
from assets_check_sel import LinkTests

if sys.platform == 'win32':
    import win_unicode_console
    win_unicode_console.enable() 
    #needed for windows because windows is stupid

test = LinkTests("http://demos.ziftsolutions.com/sample/InnovativeTechnology/?a=verizon&wid=0000000057a40d600157ba014f310317&zPage=resources-c0b4566c")
test.PDF()

"""
PDFS on SV migrated site
http://demos.ziftsolutions.com/sample/InnovativeTechnology/?a=qlik&wid=0000000056e7a7df0157066df19c1346&zPage=resources-d1ef094d

http://demos.ziftsolutions.com/sample/InnovativeTechnology/?a=verizon&wid=0000000057a40d600157ba014f310317&zPage=resources-c0b4566c

PDFS without form
http://sites.ziftsolutions.com/solid_state_solution38870/d3a6593b/EMC_Showcase_en?zPage=Hybrid-Cloud-68a5010d

PDFS with form - Epicor is unique
http://sites.ziftsolutions.com/rad_software_ltd/ad332d88/Epicor_ERP_Microsite#principle_1

More examples:
VMWare
EMC
Red Hat
CAT
Google



Ungated PDFS with Vimeo videos
http://sites.ziftsolutions.com/dmd_data_systems/f6dc4900/Product_Showcase_EN?zPage=Cloud-86b41614


Tab management
https://gist.github.com/lrhache/7686903
"""