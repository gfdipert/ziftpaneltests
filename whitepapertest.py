from splinter import Browser
import sys
import time

class LinkTests(object):

	def __init__(self,url):
		self.url = url
		self.browser = Browser('chrome')

	def GateTest(self,link):
		g_link = '?zPage='
		if g_link in link.outer_html:
			return True

	def Close(self):
		self.browser.quit()

	def WhitePaper(self):
		self.browser.visit(self.url)
		time.sleep(5)
		wp_links = self.browser.find_link_by_partial_text('White Paper: ')
		for link in wp_links:
			if not self.GateTest(link):
				if 'target="_blank"' in link.outer_html:
					title = link.text[13:]
					link.click()
					self.NewTab(link,title,self.url)
				else:
					title = link.text[13:]
					link.click()
					self.SameWindow(link,title)
			else:
				pass
			if self.GateTest(link):
				title = link.text[13:].encode('ascii','ignore')
				link.click()
				#print "This {0} is gated".format(link.text.encode('ascii', 'ignore'))
				self.FormFill(link,title)
				time.sleep(10)
				wp_links = self.browser.find_link_by_partial_text('White Paper: ')
				for link in wp_links:
					if 'target="_blank"' in link.outer_html:
						title = link.text[13:]
						link.click()
						self.NewTab(link,title,self.url)
						self.browser.visit(self.url)
						time.sleep(10)
					else:
						title = link.text[13:]
						link.click()
						self.SameWindow(link,title)
						self.browser.back()
						time.sleep(10)


	def NewTab(self,link,title,url):
		try:
			if self.browser.is_text_present(title):
				docstatus = link.text + " is linking to the correct document."
			else:
				docstatus = link.text + " is not linking to the correct document."
			print docstatus
		except:
			print "why Oops I failed with " + link.text


	def SameWindow(self,link,title):
		try:
			if self.browser.is_text_present(title):
				docstatus = link.text + " is linking to the correct document."
				print docstatus
				self.browser.back()
			else:
				docstatus = link.text + " is not linking to the correct document."
				print docstatus
				self.browser.back()
		except:
			print "Oops, I failed with " + link.text

	def FormFill(self,link,title):
		self.browser.fill('firstname','Gwen')
		self.browser.fill('lastname','Dipert')
		self.browser.fill('email','gwendipert@ziftsolutions.com')
		self.browser.fill('phone','555-555-5555')
		self.browser.fill('title','QA')
		self.browser.fill('company','Zift')
		self.browser.fill('city','Durham')
		self.browser.select('country','USA')
		self.browser.select('industry','Banking')
		self.browser.select('function','Executive')
		self.browser.find_by_value('Submit').click()







