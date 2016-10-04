import os
import sys
import time
import string
import requests
from random import randint
from screw_pdfs import convert_pdf_to_txt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from urllib2 import urlopen

#handle redirects - search in code for zStep attached to asset and href="#" only
#videos can have zStep

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

	def PDF(self):
		self.driver.get(self.url)
		WebDriverWait(self.driver,5)
		#ungated PDF
		svlinks = self.driver.find_elements_by_xpath("//li[@class='clsSVAssetType_application_pdf']/a")
		zlinks = self.driver.find_elements_by_tag_name('a')
		for svlink in svlinks:
			self.PDFTextCheck(svlink)
		for zlink in zlinks:
			try:
				if GateTest(zlink):
					zlink.click()
					submit = find_element_by_link_text('Submit')
					step = submit.get_attribute('href')
					current = self.driver.current_url
					sep = current.split('?')
					page = sep[0] + "?" + step
					self.driver.get(page)
					self.PDFTextCheck(page)	
				else:
					pass
			except:
				pass

	def PDFTextCheck(self,link):
		url = link.get_attribute('href')
		titlestring = link.text.encode('ascii','ignore')
		#exclude = set(string.punctuation)
		#nopunc = ''.join(ch for ch in titlestring if ch not in exclude)
		#titlelist = nopunc.split(" ")
		try:
			r = requests.get(url)
			status = r.status_code
			if status == 200:
				try:
					if titlestring in convert_pdf_to_txt(url):
						docstatus = "{0} is linking to the correct document.".format(titlestring)
					else:
						docstatus = "{0} is working fine but I can't find the title.".format(titlestring)
				except:
					docstatus = "I can't read {0}, but the link is working.".format(titlestring)
			else:
				docstatus = "{0} failed with status code {1}".format(titlestring, status)
		except:
			docstatus = "{0} FAILED because the domain name isn't valid".format(titlestring)
		print docstatus

	def SameWindow(self,link,title):
		url = link.get_attribute('href')
		try:
			if title in convert_pdf_to_txt(url):
				docstatus = link.text + " is linking to the correct document."
				print docstatus
				self.driver.back()
			else:
				docstatus = link.text + " is not linking to the correct document."
				print docstatus
				self.driver.back()
		except Exception as e:
			print "Oops, I failed with " + link.text
			print e

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






