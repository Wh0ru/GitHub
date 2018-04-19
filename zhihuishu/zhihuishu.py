from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

'''
.//strong[@id='popbox_title']
.//a[@class='popbtn_cancel']
.//span[@class='popup_delete j-popup-close']
.//a[@class='popbtn_yes']
.//div[@class='knowbtn_box j-popup-close']
'''

driver=webdriver.Chrome()
driver.get('https://passport.zhihuishu.com/login?service=http://online.zhihuishu.com/onlineSchool/')

username=driver.find_element_by_name('username')
password=driver.find_element_by_name('password')

# username.send_keys(input('username: '))
# password.send_keys(input('password: '))

username.send_keys('***')
password.send_keys('*****')
button=driver.find_element_by_xpath(".//span[@onclick='formSignUp();']")
button.click()

driver.switch_to_window(driver.window_handles[-1])
time.sleep(5)

b=driver.find_element_by_xpath(".//img[@src='http://image.zhihuishu.com/testzhs/createcourse/COURSE/201611/bdd0edfb1ec14ab0a44578db2b9e24e6_s2.jpg']")
b.click()

driver.switch_to_window(driver.window_handles[-1])
time.sleep(15)
try:
    no=driver.find_element_by_xpath(".//a[@class='popbtn_cancel']/span[contains(text(),'关闭')]/parent::a")
    if no:
        no.click()
        time.sleep(5)
except:
    pass
yes=driver.find_element_by_xpath(".//a[@class='popbtn_yes']")
if EC.element_to_be_clickable((By.XPATH,".//a[@class='popbtn_yes']")):
    yes.click()
    time.sleep(5)

delete=driver.find_element_by_xpath(".//span[@class='popup_delete j-popup-close']")
if EC.element_to_be_clickable((By.XPATH,".//span[@class='popup_delete j-popup-close']")):
    delete.click()

dot = driver.find_element_by_xpath(".//span[@class='videoDot examDot']")
dot_time = dot.get_attribute('timenote')
d=int(dot_time.split(':')[1])*60+int(dot_time.split(':')[2])
all=driver.find_element_by_xpath(".//div[@class='progressbar']/parent::div/preceding-sibling::span[1]")
a=int(all.text.split(':')[1])*60+int(all.text.split(':')[2])
c=int(d/a)
p=driver.find_element_by_xpath(".//div[@class='progressbar']")
s=p.get_attribute('style')
s=int(s.split(':')[1].split('.')[0].replace(' ','').replace('%;',''))
wait_time = (int(dot_time.split(':')[1]) * 60 + 60)
if c>s:
    wait = WebDriverWait(driver, wait_time)
    no = wait.until(EC.element_to_be_clickable((By.XPATH, ".//a[@class='popbtn_cancel']")))
    no.click()
elif s>=c:
    time.sleep(a-d+10)

while True:
    progress=driver.find_element_by_xpath(".//div[@class='progressbar']")
    style=progress.get_attribute('style')
    all_time=driver.find_element_by_xpath(".//div[@class='progressbar']/parent::div/preceding-sibling::span[1]")
    if '100' in style:
        next_video=driver.find_element_by_xpath(".//div[@class='progressbar']/parent::div/parent::li/following-sibling::li")
        if next_video.get_attribute('id')=='video-0':
            n = driver.find_element_by_xpath(".//div[@class='progressbar']/parent::div/parent::li/following-sibling::li[2]")
            n.click()
        elif next_video.get_attribute('title')=='点击测试':
            n=driver.find_element_by_xpath(".//div[@class='progressbar']/parent::div/parent::li/following-sibling::li[4]")
            n.click()
        else:
            next_video.click()
            time.sleep(5)
    else:
        dot = driver.find_element_by_xpath(".//span[@class='videoDot examDot']")
        dot_time = dot.get_attribute('timenote')
        wait_time = (int(dot_time.split(':')[1]) * 60 + 60)

        wait = WebDriverWait(driver, wait_time)
        no = wait.until(EC.element_to_be_clickable((By.XPATH, ".//a[@class='popbtn_cancel']")))
        no.click()
        t=int(all_time.text.split(':')[1])-int(dot_time.split(':')[1])+60
        time.sleep(t)



# driver.switch_to_window(driver.window_handles[-2])
# time.sleep(5)
# t=driver.find_element_by_xpath(".//img[@src='http://image.zhihuishu.com/testzhs/createcourse/COURSE/201611/757001066d1345fe865b70e240d20f8d_s2.jpg']")
# driver.switch_to_window(driver.window_handles[-1])
# yes=driver.find_element_by_xpath(".//a[@class='popbtn_yes']")
# if EC.element_to_be_clickable((By.XPATH,".//a[@class='popbtn_yes']")):
#     yes.click()
#     time.sleep(5)
# # delete=driver.find_element_by_xpath(".//span[@class='popup_delete j-popup-close']")
# delete=driver.find_element_by_xpath(".//span[@class='popup_delete j-popup-close']")
# if EC.element_to_be_clickable((By.XPATH,".//span[@class='popup_delete j-popup-close']")):
#     delete.click()



# driver=webdriver.PhantomJS()
# driver.get('http://course.zhihuishu.com/learning/videoList?courseId=2023108&rid=6629')
# driver.save_screenshot('login.png')
#
# driver.close()
# driver.quit()
