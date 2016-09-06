import os
import sys
import time
import screw_pdfs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from urllib2 import urlopen

class LinkTests(object):

	def __init__(self,url):
		self.url = url
		chromedriver = "C:\Users\Gwen Dipert\Documents\chromedriver.exe"
		os.environ["webdriver.chrome.driver"] = chromedriver
		self.driver = webdriver.Chrome(chromedriver)
		self.driver.get(url)

	def GateTest(self,link):
		if '?zPage=' in link.get_attribute("href"):
				return True

	def Close(self):
		self.driver.close()

	def WhitePaper(self):
		self.driver.get(self.url)
		element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "Panel Scripts")))
		wp_links = self.driver.find_elements_by_partial_link_text('White Paper: ')
		for link in wp_links:
			if not self.GateTest(link):
				if "_blank" in link.get_attribute("target"):
					title = link.text[22:]
					link.click()
					self.NewTab(link,title,self.url)
				else:
					title = link.text[22:]
					link.click()
					self.SameWindow(link,title)
			else:
				pass
			if self.GateTest(link):
				title = link.text[22:].encode('ascii','ignore')
				link.click()
				#print "This {0} is gated".format(link.text.encode('ascii', 'ignore'))
				self.FormFill()
				WebDriverWait(self.driver,5)
				wp_links = self.driver.find_elements_by_partial_link_text('White Paper: ')
				for link in wp_links:
					if "_blank" in link.get_attribute("target"):
						title = link.text[22:]
						link.click()
						self.NewTab(link,title,self.url)
						self.driver.execute_script("window.open(" + self.url + ");")
						WebDriverWait(self.driver,5)
					else:
						title = link.text[22:]
						link.click()
						self.SameWindow(link,title)

	def NewTab(self,link,title,url):
		url = link.get_attribute('href')
		print url
		print title
		try:
			if title in screw_pdfs.convert_pdf_to_txt(url):
				print screw_pdfs.convert_pdf_to_txt(url)
				docstatus = link.text + " is linking to the correct document."
			else:
				docstatus = link.text + " is not linking to the correct document."
			print docstatus
		except:
			print "Oops I failed with " + link.text


	def SameWindow(self,link,title):
		url = link.get_attribute('href')
		try:
			if title in screw_pdfs.convert_pdf_to_txt(url):
				docstatus = link.text + " is linking to the correct document."
				print docstatus
				self.driver.back()
			else:
				docstatus = link.text + " is not linking to the correct document."
				print docstatus
				self.driver.back()
		except:
			print "Oops, I failed with " + link.text

	def FormFill(self):
		self.driver.find_element_by_id("firstname").send_keys("gwen")
		self.driver.find_element_by_id("lastname").send_keys("dipert")
		self.driver.find_element_by_id("email").send_keys("email@test.com")
		self.driver.find_element_by_id("phone").send_keys("555-555-5555")
		self.driver.find_element_by_id("title").send_keys("QA")
		self.driver.find_element_by_id("company").send_keys("Zift")
		self.driver.find_element_by_id("city").send_keys("Durham")
		select = Select(self.driver.find_element_by_id("country"))
		select.select_by_visible_text("USA")
		select = Select(self.driver.find_element_by_id("industry"))
		select.select_by_visible_text("Banking")
		select = Select(self.driver.find_element_by_id("function"))
		select.select_by_visible_text("Executive")
		self.driver.find_element_by_link_text('Submit').click()









