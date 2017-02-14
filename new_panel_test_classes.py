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

class ResourceTest(object):

	def __init__(self,url):
		self.url = url
		self.driver = webdriver.Chrome()
		self.driver.get(url)

	def GateTest(self,link):
		if link.get_attribute('ng-if') == "RES.RGatedOption.indexOf('No') == -1":
			return True

	def GetResourceURL(self,link):
		asset = self.driver.find_element_by_id("ConfirmationAsset")
		href = asset.get_attribute('href')

	def FormSubmit(self):
		download = self.driver.find_element_by_xpath("//a[contains(@ng-click, 'getConfirmation()')]")
		download.click()

	def Close(self):
		self.driver.close()

	def Resource(self):
		#element = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(@class, 'z_btn z_btn-primary zpersonModal ng-binding ng-scope)]")))
		#element = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.LINK_TEXT,"Download")))
		gated = []
		links = self.driver.find_elements_by_xpath("//a[contains(@ng-click, 'getForm(RES)')]")
		print links
		for link in links:
			if self.GateTest(link):
				gated.append(link)
			else:
				pass
		for gate in gated:
			gate.click()
			self.FormFill()
			self.FormSubmit()
			resourcename = self.driver.find_element_by_xpath("//div/span[contains(@class, 'AssetTitle')]").text.encode('ascii','ignore')
			asset = self.driver.find_element_by_id("ConfirmationAsset")
			href = asset.get_attribute('href')
			self.PDFTextCheck(resourcename,href)

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
		self.driver.find_element_by_id("first_name").send_keys("First_Name")
		self.driver.find_element_by_id("last_name").send_keys("Last_Name")
		self.driver.find_element_by_id("email").send_keys("name@ziftsolutions.com")