from DrissionPage import ChromiumPage
import time
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def scrape():
    website = ChromiumPage()
    website.get('https://visa.vfsglobal.com/arg/en/dnk/book-appointment')
    
    # Wait for Cloudflare challenge
    i = website.get_frame('@src^https://challenges.cloudflare.com/cdn-cgi')
    if i:
        e = i('.mark')
        time.sleep(15)
        e.click()

    # Input credentials and sign in
    inputting = website.ele('tag:input@id:email')
    inputting.input("USER")
    time.sleep(3)
    inputting2 = website.ele('tag:input@id:password')
    inputting2.input('PASSWORD')
    time.sleep(5)
    website.ele('Sign In').click()
    time.sleep(8)
    
    # Start new booking and select sub-category
    try:
        website.ele('@class=mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base').click('js')
    except:
        print("No Start New Booking button found.")
        website.ele('@class=mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base').click('js')
    time.sleep(5)
    website.ele('Select your sub-category').click()
    website.ele(' Work Permit - ').click()
    time.sleep(5)

    # Continue and fill form details
    try:
        website.ele('Continue').click('js')
    except:
        print("Continue button not found.")
        website.ele('Continue').click('js')
    time.sleep(5)

    # Fill personal details
    website.ele('@placeholder=Enter your first name').input('ADYLBEK')
    website.ele('@placeholder=Please enter last name.').input('ZHUNUSOV')
    time.sleep(5)
    website.ele('@role=combobox').click()
    website.ele(' KYRGYZSTAN ').click()
    time.sleep(5)
    website.ele('@placeholder=Enter passport number').input('ID')
    time.sleep(5)
    website.ele('@placeholder=Please select the date').input('DATE')
    website.ele('@placeholder=44').input('COUNTRYNUMBER')
    website.ele('@placeholder=012345648382').input('PHONE NUMBER')
    time.sleep(10)
    website.ele('@placeholder=Enter Email Address').input('MAIL')
    time.sleep(5)

    try:
        website.ele('Save').click('js')
    except:
        print("Save button not found.")
        website.ele('Save').click('js')
    try:
        website.ele(' Continue ').click('js')
    except:
        print("Continue button not found.")
        website.ele(' Continue ').click('js')

    # Collect available dates by navigating the calendar
    soap_list = {}
    for _ in range(3):
        soap = BeautifulSoup(website.html, 'lxml')
        soap_list[soap.find(class_="fc-toolbar-title").text] = soap
        website.ele('@aria-label=next').click()
        time.sleep(5)

    # Process available dates
    for month, soap in soap_list.items():
        available_days = soap.findAll('a', class_='fc-daygrid-event fc-daygrid-block-event fc-h-event fc-event fc-event-start fc-event-end fc-event-future availiable')
        dates = {day.parent.parent.find_previous_sibling('div').text for day in available_days}
        soap_list[month] = list(dates)

    return soap_list

@app.route('/scrape', methods=['GET'])
def scrape_endpoint():
    try:
        result = scrape()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
