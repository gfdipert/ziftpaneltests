import sys
from assets_check_sel import LinkTests

if sys.platform == 'win32':
    import win_unicode_console
    win_unicode_console.enable() 
    #needed for windows because windows is stupid

test = LinkTests("http://demos.ziftsolutions.com/sample/InnovativeTechnology/?a=qlik&wid=ff808181569b6fc10156a08e41a334b7&zPage=resources-d1ef094d")
test.PDF()

"""
PDFS without form
http://sites.ziftsolutions.com/solid_state_solution38870/d3a6593b/EMC_Showcase_en?zPage=Hybrid-Cloud-68a5010d

PDFS with form
http://sites.ziftsolutions.com/rad_software_ltd/ad332d88/Epicor_ERP_Microsite#principle_1

Ungated PDFS with Vimeo videos
http://sites.ziftsolutions.com/dmd_data_systems/f6dc4900/Product_Showcase_EN?zPage=Cloud-86b41614
"""