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
			if 'pdf' in zlink.get_attribute('href'):
				r = requests.get(zlink.get_attribute('href'))
				status = r.status_code
				if status == 200:
					print "{0} was successful".format(zlink.text.encode('ascii','ignore'))
				else:
					print "{0} FAILED WITH STATUS CODE {1}".format(zlink.text.encode('ascii','ignore'), status)
			else:
				pass

	def PDFTextCheck(self,link):
		url = link.get_attribute('href')
		titlestring = link.text.encode('ascii','ignore')
		exclude = set(string.punctuation)
		nopunc = ''.join(ch for ch in titlestring if ch not in exclude)
		titlelist = nopunc.split(" ")
		i = randint(0,len(titlelist)-3)
		title = titlelist[i] + " " + titlelist[i+1]
		try:
			if title in convert_pdf_to_txt(url):
				docstatus = link.text + " is linking to the correct document."
			else:
				docstatus = link.text + " is not linking to the correct document."
			print docstatus
		except Exception as e:
			print "Oops I failed with " + link.text

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






