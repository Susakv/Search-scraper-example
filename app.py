from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep 
from selenium.webdriver.chrome.options import Options
import time
from flask import Flask, session, render_template, request, g, redirect, send_file
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def input_window():
    return render_template("UI.html")

@app.route("/input_record", methods= ["GET", "POST"])
def get_query():
    if request.method == 'GET':
        return render_template('UI.html')
    else:
        form_output = (request.form['query'])

        url = 'https://www.google.com/search?q='+ form_output +'&hl=cs&source=hp&ei=GzOJY9mHFbPc7_UPudGq2AM&iflsig=AJiK0e8AAAAAY4lBKxhb8SF9_pDJdP4fD8keZd8dYmxK&ved=0ahUKEwiZgdCAxNn7AhUz7rsIHbmoCjsQ4dUDCAg&uact=5&oq=cuketa&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEIAEMgsILhCABBCxAxDUAjIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgsIABCABBCxAxCDAToICAAQgAQQsQM6EQguEIAEELEDEIMBEMcBENEDOhEILhCDARDHARCxAxDRAxCABDoOCC4QgAQQsQMQxwEQ0QM6CwguEIMBELEDEIAEOhEILhCABBCxAxCDARDHARCvAToOCC4QgwEQ1AIQsQMQgARQAFjOC2CiEGgAcAB4AIAB4wKIAaQIkgEHMC40LjEuMZgBAKABAQ&sclient=gws-wiz'

        driver = webdriver.Chrome()
        driver.get(url)
        try:
            element = WebDriverWait(driver, 0).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://consent.google.com']")))
            WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='introAgreeButton']"))).click()
        finally:
            soup = BeautifulSoup(driver.page_source,'html.parser')
            items = soup.find_all('div',{'class':'MjjYud'})
            
            items_string = str(items)
            #return items_string
            html_file = open("record.html","w")
            html_file.write(items_string)
            html_file.close()
            txt_file = open("record.txt", "w")
            txt_file.write(items_string)
            txt_file.close
            driver.quit()

            return redirect("/result_display")

@app.route("/result_display")
def result_display():
    return render_template("result_display.html")

@app.route("/file_download")
def file_download():
    return send_file("record.html")

if __name__ == '__main__':
    app.run(debug=True)