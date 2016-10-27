import os
import sys
import time
import requests
from screw_pdfs import convert_pdf_to_txt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from urllib2 import urlopen

class LinkTests(object):

	global PDFpages
	PDFpages = []

	def __init__(self,url):
		self.url = url
		chromedriver = "C:\Users\Gwen Dipert\Documents\chromedriver.exe"
		os.environ["webdriver.chrome.driver"] = chromedriver
		self.driver = webdriver.Chrome(chromedriver)
		self.driver.get(url)
		self.handle = self.driver.current_window_handle

	def GateTest(self,link):
		if '?zPage=' in link.get_attribute("href"):
				return True

	def GetPDFURL(self,link):
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
		print formpage
		submit = self.driver.find_element_by_link_text('Submit')
		step = submit.get_attribute('href').split('?')
		current = self.driver.current_url.split('?')
		page = current[0] + "?" + step[1]
		self.driver.get(page)
		WebDriverWait(self.driver,5)
		links = self.driver.find_elements_by_tag_name('a')
		PDFstatus = ""
		for link in links:
			href = link.get_attribute('href')
			if "pdf" in href:
				try:
					self.PDFTextCheck(link)
					PDFstatus = "PDFSPRESENT"
				except:
					pass
			else:
				pass
		if PDFstatus == "":
			print "There are no PDFs on this page."

	def Close(self):
		self.driver.close()

	def PDF(self):
		self.driver.get(self.url)
		WebDriverWait(self.driver,10)
		svparents = self.driver.find_elements_by_tag_name('li')
		for svparent in svparents:
			if "clsSVAssetType_application_pdf" in svparent.get_attribute('class'):
				svlink = svparent.find_element_by_tag_name('a')
				self.PDFTextCheck(svlink)
			else:
				pass
		zlinks = self.driver.find_elements_by_tag_name('a')
		for zlink in zlinks:
			try:
				if 'pdf' in zlink.get_attribute('href'):
					try:
						self.PDFTextCheck(zlink)
					except:
						pass
				elif self.GateTest(zlink):
					self.GetPDFURL(zlink)
				else:
					pass
			except:
				pass
		windows = self.driver.window_handles
		numwindows = len(self.driver.window_handles)
		print numwindows
		i = 1
		self.driver.switch_to_window(windows[1])
		while i < numwindows:
			self.PDFFormSubmit()
			i += 1
			if i == numwindows:
				pass
			else:
				self.driver.switch_to_window(windows[i])


	def PDFTextCheck(self,link):
		url = link.get_attribute('href')
		titlestring = link.text.encode('ascii','ignore')
		titletest = titlestring[:4]
		try:
			r = requests.get(url)
			status = r.status_code
			if status == 200:
				try:
					if titletest in convert_pdf_to_txt(url):
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






