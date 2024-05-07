import csv
import time
import sys


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


from selenium.webdriver.chrome.service import Service




from bs4 import BeautifulSoup


dictionary_data = {}
current_db = ""
current_link = ""
current_records = 0


# constants
records_target_limit = 400
#select the DB and login of your choice here and than run the script to save the data
#akb libId = [schaumburg "50", lemont "29","45"]
libId = ["50"]
#akb libcode = [sch "21257009503617","21559000784895","21565000784895"]                                                                         1of4 LIBRARIES
libcode = ["21257009503617"]
lib_index = 0
db_index = 2


#System.setProperty("webdriver.edge.driver", "c://Users//abern//Documents//Python Programs//RIS//msedgedriver.exe");


#DRIVER_PATH = 'C://Users//abern//Documents//Python Programs//RIS//msedgedriver.exe'
DRIVER_PATH = "msedgedriver.exe"
                  
def start_driver_again():
    driver =  webdriver.Edge()
    while(True):
        try:
            driver.get("http://beta-liboff.public-record.com/remote/results")
            wait = WebDriverWait(driver, 10)
            libraryid_dd = driver.find_element("xpath",'//select[@id="library_id"]/option[@value='+libId[lib_index]+']').click()
            library_value_tb = driver.find_element("id","library_value")
            library_value_tb.clear()
            library_value_tb.send_keys(libcode[lib_index])
            find_library_btn = driver.find_element("xpath",'//div/button[@name="Submit"]').click()
            break
        except Exception as e:
            print(e)
            print("Check internet connection.")
            time.sleep(15)
    current_url = 'https://beta-liboff.public-record.com/databases'
    driver.get(current_url)
    try:
        wait = WebDriverWait(driver, 10)
        driver.find_element("xpath",'//a[@href="/databases/'+current_db+'"]').click()
        wait = WebDriverWait(driver, 5)
    except:
        print("DB doesn't exist.")
    try:
        driver.find_element("xpath",'//a[@href="/databases/' + current_db + '/set/'+current_link+'/"]').click()
    except Exception as e:
        print(e)
    #DATE SEARCH BLOCK OF CODE mandatory ...........................................                      ALTERNATIVE DATES
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sdate")))
        elem = driver.find_element("name","sdate")
        elem.clear()
        elem.send_keys("12/23/2022")
        elem = driver.find_element("name","edate")
        elem.clear()
        elem.send_keys("12/23/2022")
    #FORECLOSURE SALE DATE SEARCH ONLY
        elem = driver.find_element("name","sdate2")
        elem.clear()
        elem.send_keys("11/17/2022")
        elem = driver.find_element("name","edate2")
        elem.clear()
        elem.send_keys("11/24/2028")
              
        select = Select(driver.find_element("name",'city_1'))
        #select.select_by_visible_text('Dolton')
    except:
        pass
    #TAX REDEMTION DATE SEARCH ONLY
    #elem = driver.find_element("name","resdate")
    #elem.clear()
    #elem.send_keys("02/12/2023")
    #elem = driver.find_element("name","redate")
    #elem.clear()
    #elem.send_keys("10/02/2029")
                    
    #elem = driver.find_element("name",sdate2")
    #elem.clear()
    #elem.send_keys("05/11/2022")
    #elem = driver.find_element("name",edate2")
    #elem.clear()
    #elem.send_keys("05/10/2027")
    #DATE SEARCH BLOCK OF CODE mandatory...........................................


    #TAX REDEMTION DATE SEARCH ONLY (optional) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!                    
    #elem = driver.find_element("name",resdate")
    #elem.clear()
    #elem.send_keys("04/07/2022")
    #elem = driver.find_element("name",reedate")
    #elem.clear()
    #elem.send_keys("02/28/2028")
    #TAX REDEMTION DATE SEARCH ONLY (optional) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    
    #FORECLOSURE SALE DATE SEARCH ONLY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #elem = driver.find_element("name",sdate2")
    #elem.clear()
    #elem.send_keys("05/11/2022")
    #elem = driver.find_element("name",edate2")
    #elem.clear()
    #elem.send_keys("05/10/2027")
    #FORECLOSURE SALE DATE SEARCH ONLY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!                                                        
    #time.sleep(60)


    driver.find_element("xpath",'.//input[@value="Find Data"]').click()
    wait = WebDriverWait(driver, 10)
    driver.find_element("xpath",'//input[@value="Run Report"]').click()
    return driver


def scrapRecords(driver, file_name):
    global current_records
    print("Starting records scraping")
    total_records = 0
    write_header = True
    mode = "w"
    try:
        total_records = int(str(driver.find_element("xpath",'//span[@class="show_record_count"]').text).replace(",",""))
    except:
        total_records = 0
        pass
    basic_url = driver.current_url
    print("Total records", total_records)


    records = 1
    while records <= total_records:
        if(current_records == records_target_limit):
            driver.close()
            driver = start_driver_again()
            current_records = 0
        try:
            if(records == 1):
                driver.get(str(basic_url))
            else:
                driver.get(str(basic_url)+"/"+str(records))
        except:
            print("Reloading the record")
            time.sleep(5)
            driver.refresh()
            time.sleep(5)
            records -= 1
            continue
        try:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            soup = soup.find("div", {"class" : "record"})
            for tr in soup.find_all("tr"):
                tds = tr.find_all("td")
                #print("the soup pre if", file_name)
                if(len(tds) > 1):
                        #print("the soup post if", str(tds[1].text).strip() )
                        dictionary_data[str(tds[0].text)] = str(tds[1].text).strip()
        except:
            driver.quit()
            driver = webdriver.Edge(executable_path=DRIVER_PATH)
        with open(file_name+'_details.csv','a', encoding='utf8', newline='') as csvfile:
            if (write_header):
                fieldnames = dictionary_data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                write_header = False
                mode = 'a'
            else:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dictionary_data)
        print(records)
        records+=1
        current_records = current_records + 1
    return driver


def main():
  #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  
  driver = webdriver.Edge()
  global current_db
  global current_link
  #db = ["foreclosures","taxsales","probate","buildingviolations","realestate",]
  ############### WARNING - Building voilations is for Chicago only   ##############################                                              
  #db = ["buildingviolations","taxsales"]




####################################################################################################################################


  #db = ["taxsales"]
  db = ["probate"]
#                                                                                                                                                     2of4 DATABASES  
  #db = ["buildingviolations"]
  #db = ["realestate"]




####################################################################################################################################  
  while(True):
        try:
            driver.get("http://beta-liboff.public-record.com/remote/results")
            wait = WebDriverWait(driver, 10)
            libraryid_dd = driver.find_element("xpath",'//select[@id="library_id"]/option[@value='+libId[lib_index]+']').click()
            library_value_tb = driver.find_element("id","library_value")
            library_value_tb.clear()
            library_value_tb.send_keys(libcode[lib_index])
            find_library_btn = driver.find_element("xpath",'//div/button[@name="Submit"]').click()
            break
        except Exception as e:
            print(e)
            print("Check internet connection.")
            time.sleep(15)
  current_url = 'https://beta-liboff.public-record.com/databases'
  for dbs in db:
        driver.get(current_url)
        current_db = dbs
        while(True):
            try:
                wait = WebDriverWait(driver, 10)
                driver.find_element("xpath",'//a[@href="/databases/'+dbs+'"]').click()
                wait = WebDriverWait(driver, 5)
                current_db_url = driver.current_url
            except:
                print("DB doesn't exist.")
            break
  ############### WARNING - Building voilations is for Chicago only   ##############################                                             


        #links = ["cook","dekalb","dupage","kane","kendall","lake","McHenry","will","winnebago"]                                               
        #links = ["will"]
















####################################################################################################################################


        #links  = ["winnebago"]                                                      


#                                                                                                                                                           3of4 COUNTIES


        links = ["cook","dekalb","dupage","kane","kendall","lake","McHenry","will","winnebago"]         
        
####################################################################################################################################
















        for x in range(0,len(links)):
          try:
            current_link = links[x]
            print("Current link: ", current_link)
            #comment "driver.find_element("xpath",'//a[@href="/databases/' + dbs + '/set/'+links[x]+'"]').click()" for code violations
            wait = WebDriverWait(driver, 10)
            #if dbs != 'buildingviolations':
            if dbs != 'detainers' and dbs != 'buildingviolations':
              try:
                driver.find_element("xpath",'//a[@href="/databases/' + dbs + '/set/'+links[x]+'/"]').click()
              except Exception as e:
                print(e)
                continue
            #DATE SEARCH BLOCK OF CODE mandatory ...........................................                                                
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sdate")))
            elem = driver.find_element("name","sdate")
            elem.clear()








####################################################################################################################################


            elem.send_keys("4/21/2024")
            elem = driver.find_element("name","edate")
#                                                                                                                                                          4of4 DATES            
            elem.clear()
            elem.send_keys("1/21/2026")
                    
####################################################################################################################################












            #FORECLOSURE SALE DATE SEARCH ONLY
            try:
              elem = driver.find_element("name","sdate2")
              elem.clear()
              elem.send_keys("00/00/0000")
              elem = driver.find_element("name","edate2")
              elem.clear()
              elem.send_keys("00/00/0000")
              
              select = Select(driver.find_element("name",'city_1'))
              #select.select_by_visible_text('Dolton')
            except:
              pass
            #TAX REDEMTION DATE SEARCH ONLY
            #elem = driver.find_element("name","resdate")
            #elem.clear()
            #elem.send_keys("09/03/2022")
            #elem = driver.find_element("name","redate")
            #elem.clear()
            #elem.send_keys("10/02/2022")
                    
            #elem = driver.find_element("name",sdate2")
            #elem.clear()
            #elem.send_keys("05/11/2022")
            #elem = driver.find_element("name",edate2")
            #elem.clear()
            #elem.send_keys("05/10/2027")
            #DATE SEARCH BLOCK OF CODE mandatory...........................................


            #TAX REDEMTION DATE SEARCH ONLY (optional) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!                    
            #elem = driver.find_element("name",resdate")
            #elem.clear()
            #elem.send_keys("04/07/2022")
            #elem = driver.find_element("name",reedate")
            #elem.clear()
            #elem.send_keys("02/28/2028")
            #TAX REDEMTION DATE SEARCH ONLY (optional) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
                    
            #FORECLOSURE SALE DATE SEARCH ONLY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #elem = driver.find_element("name",sdate2")
            #elem.clear()
            #elem.send_keys("05/11/2022")
            #elem = driver.find_element("name",edate2")
            #elem.clear()
            #elem.send_keys("05/10/2027")
            #FORECLOSURE SALE DATE SEARCH ONLY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!                                                      
            temp4 = input('                                                                PRESS ON THE CONSOLE WHEN READY\n')
            #time.sleep(60)


            driver.find_element("xpath",'.//input[@value="Find Data"]').click()
            wait = WebDriverWait(driver, 10)
            driver.find_element("xpath",'//input[@value="Run Report"]').click()
            driver = scrapRecords(driver, libId[lib_index] + "_" + dbs+"_"+links[x])
            wait = WebDriverWait(driver, 10)
            driver.get(current_db_url)
          except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            driver.refresh()
            time.sleep(8)
        
main()