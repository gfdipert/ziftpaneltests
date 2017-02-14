import os
import sys
import time
import requests
import re
import urllib3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from urllib2 import urlopen
from urlparse import urlsplit
from urlparse import urlparse
import urllib3.contrib.pyopenssl
from screw_pdfs import convert_pdf_to_txt

class LinkTests(object):

	global PDFpages
	PDFpages = []

	def __init__(self,url):
		self.url = url
		#chromedriver = "/Users/gwendipert/Documents/chromedriver"
		#os.environ["webdriver.chrome.driver"] = chromedriver
		self.driver = webdriver.Chrome()
		self.driver.get(url)
		#self.handle = self.driver.current_window_handle

	def GateTest(self,link):
		if '?zPage=' in link.get_attribute("href"):
			return True

	def GetFormURL(self,link):
		formbit = link.get_attribute('href').split('?')
		formpage = self.driver.current_url.split('#')[0] + "?" + formbit[1]
		if formpage not in PDFpages:
			PDFpages.append(formpage)
			script = '''window.open("{0}", "_blank");'''.format(formpage)
			self.driver.execute_script(script)
		else:
			return

	def PDFFormSubmit(self):
		element = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.LINK_TEXT,"Submit")))
		formpage = self.driver.current_url
		submit = self.driver.find_element_by_link_text('Submit')
		step = submit.get_attribute('href').split('?')
		current = self.driver.current_url.split('?')
		del current[len(current)-1]
		page = ''.join(current) + "?" + step[len(step)-1]
		self.driver.get(page)
		WebDriverWait(self.driver,5)
		links = self.driver.find_elements_by_tag_name('a')
		PDFstatus = ""
		for link in links:
			href = link.get_attribute('href').encode('ascii','ignore')
			if 'pdf' in href.split('.'):
				title = link.text.encode('ascii','ignore')
				print self.driver.current_url
				self.PDFTextCheck(title,href)
				PDFstatus = "PDF"
			else:
				pass
		if PDFstatus == "":
			print self.driver.current_url
			print "There are no PDFs on this page."

	def Close(self):
		self.driver.close()

	def PDF(self):
		self.driver.get(self.url)
		zlinks = self.driver.find_elements_by_xpath("//span[@name='RES.Resource Name']/ancestor::*[position()=1]")
		zlinknames = self.driver.find_elements_by_xpath("//span[@name='RES.Resource Name']")
		for zlink in zlinks:
			for zlinkname in zlinknames:
				zlinktitle = zlinkname.get_attribute('innerHTML')
				href = zlink.get_attribute('href')
				if 'pdf' in href.split('.'):
					#href = href.replace('https://','http://')
					self.PDFTextCheck(zlinktitle,href)
				else:
					pass

	def PDFTextCheck(self,title,href):
		try:
			r = requests.get(href)
			status = r.status_code
			if status == 200:
				try:
					if title in convert_pdf_to_txt(href):
						docstatus = "{0} is linking to the correct document.".format(title)
					else:
						docstatus = "{0} is working fine but I can't find the title.".format(title)
				except:
					docstatus = "I can't read {0}, but the link is working.".format(title)
			else:
				docstatus = "{0} failed with status code {1}".format(title, status)
		except:
			docstatus = "{0} FAILED because the domain name isn't valid".format(title)
		print docstatus

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