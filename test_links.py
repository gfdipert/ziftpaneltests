import sys
from assets_check_sel import LinkTests

if sys.platform == 'win32':
    import win_unicode_console
    win_unicode_console.enable() 
    #needed for windows because windows is stupid

test = LinkTests("http://samples.zift123.com/?aa=vmware.ziftsolutions.com&wid=0000000057536d62015767a5d7755bbd&zPage=vRealize-Log-Insight-bd041a5d")
test.PDF()

"""
PDFS on SV migrated site
	http://demos.ziftsolutions.com/sample/InnovativeTechnology/?a=qlik&wid=0000000056e7a7df0157066df19c1346&zPage=resources-d1ef094d

	http://demos.ziftsolutions.com/sample/InnovativeTechnology/?a=verizon&wid=0000000057a40d600157ba014f310317&zPage=resources-c0b4566c

PDFS without form

	EMC
	http://sites.ziftsolutions.com/solid_state_solution38870/d3a6593b/EMC_Showcase_en?zPage=Hybrid-Cloud-68a5010d - Works, for the most part.  Doesn't ignore breadcrumb links.

	Dell APJ
	http://samples.zift123.com/?aa=dell.ziftsolutions.com&wid=ff80818157e29ef001580189791a6da9&zPage=Resources-126c5928 - WORKS!

PDFS with form
	Epicor (unique case)
	http://sites.ziftsolutions.com/rad_software_ltd/ad332d88/Epicor_ERP_Microsite#principle_1 - WORKS!

	VMware
	hhttp://samples.zift123.com/?aa=vmware.ziftsolutions.com&wid=0000000057536d62015767a5d7755bbd&zPage=Try-VMware-56310845
	
PDFS with form in Modal
	http://samples.zift123.com/?aa=emc.ziftsolutions.com&wid=ff808181578b4a7b01579165a4d133a8&zPage=VNX-672a010a

More examples:

EMC
Red Hat
CAT
Google

Ungated PDFS with Vimeo videos
http://sites.ziftsolutions.com/dmd_data_systems/f6dc4900/Product_Showcase_EN?zPage=Cloud-86b41614

Additional cases:
- handle redirects - search in code for zStep attached to asset and href="#" only
- videos can have zStep

navs = self.driver.find_elements_by_xpath(".//*[ancestor::div[@class='z_nav']]")

"""
