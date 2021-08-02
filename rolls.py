from random import randrange
import json
from pandas import *
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

def arrayFixer(array):
    fixed = []
    previousName = None
    for name in array: 
        if name == None:
            fixed.append(previousName)
        else:
            x = name.replace(":", "")
            fixed.append(x)
            previousName = x
            
    return fixed

def nameFinder(num):
    num -= 1
    try:
        name = driver.find_element_by_xpath(f'/html/body/div[5]/div/div[{num}]/span[2]').get_attribute("innerHTML")
        return name
    except:
        nameFinder(num)

def cleanResult(result):
    if "critsuccess" in result:
        return 20
    elif "critfail" in result:
        return 1
    
    else:
        x = range(20,1,-1)
        for y in x:
            if "basicdiceroll\">" + str(y) in result:
                return y
            else:
                continue
            
def dictMaker(n,s,r,p):
    tempDict = {
    "Name": n,
    "Skill": s,
    "Result": r,
    "Points": p
    }
    return tempDict
    


driver = webdriver.Firefox()

data = read_csv("iofiles/skills.csv")
abilites = data['abilites'].tolist()

with open("iofiles/credentials.txt", "r") as file:
    data = file.readlines()
    
user = data[0]

password = data[1]

driver.get("https://app.roll20.net/sessions/new")

driver.find_element_by_id("email").send_keys(user)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("login").click()

WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)

driver.get("https://app.roll20.net/campaigns/chatarchive/1777961/?p=2&onePage=&hidewhispers=true&hiderollresults=true")

sleep(2)
nameArray = []
skillArray = []
resultArray = []
x = range(1,1000)
for y in x:
    try:
        skill = driver.find_element_by_xpath(f'/html/body/div[5]/div/div[{y}]/div/div/div[2]/div[2]/span/span[1]').get_attribute("innerHTML")
        result = driver.find_element_by_xpath(f'/html/body/div[5]/div/div[{y}]/div/div/div[2]/div[4]/div/span/span').get_attribute("title")

        for ability in abilites:
            if skill == ability:
                skillArray.append(skill)
                resultArray.append(cleanResult(result))
                try:
                    name = driver.find_element_by_xpath(f'/html/body/div[5]/div/div[{y}]/span[2]').get_attribute("innerHTML") 
                    nameArray.append(name)
                except:
                    if len(nameArray) < len(skillArray):
                        nameArray.append(nameFinder(y))
                    else:
                        continue                      
    except:
        continue
    

for y in x:
    try:
        skill = driver.find_element_by_xpath(f'/html/body/div[5]/div/div[{y}]/div/div/div[2]/div[4]/div/div[1]/span/a').get_attribute("innerHTML")
        result = driver.find_element_by_xpath(f'/html/body/div[5]/div/div[{y}]/div/div/div[2]/div[4]/div/div[2]/span[1]/span').get_attribute("title")

        for ability in abilites:
            if skill == ability:
                skillArray.append(skill.replace(":",""))
                resultArray.append(cleanResult(result))
                try:
                    name = driver.find_element_by_xpath(f'/html/body/div[5]/div/div[{y}]/span[2]').get_attribute("innerHTML") 
                    nameArray.append(name)
                except:
                    if len(nameArray) < len(skillArray):
                        nameArray.append(nameFinder(y))
                    else:
                        continue
    except:
        continue
    
for y in x:
    try:
        spell = driver.find_element_by_xpath(f'/html/body/div[5]/div/div[{y}]/div/div/div[2]/div[3]/div').text
        if "level" in spell:
            skillArray.append("Spellslot Attack")
            resultArray.append(randrange(1,21))
            try:
                name = driver.find_element_by_xpath(f'/html/body/div[5]/div/div[{y}]/span[2]').get_attribute("innerHTML") 
                nameArray.append(name)
            except:
                if len(nameArray) < len(skillArray):
                    nameArray.append(nameFinder(y))
                else:
                    continue        
    except:
        continue


#print(f'{nameArray} {len(nameArray)}') 
#print(f'{skillArray} {len(skillArray)}')
#print(f'{resultArray} {len(resultArray)}')   
 
nameArray = arrayFixer(nameArray)
 
dictList = []  
for n, s, r in zip(nameArray, skillArray, resultArray):
    n.replace(":", "")
    if "(To" in n:
        continue
    elif "(GM)" in n:
        continue
    if "Attack" in s:
        if r == 20:
            dictList.append(dictMaker(n,s,r,1))
            
        else:
            continue
    elif r >= 16:
        p = 1
        if r == 20:
            p = 2
        dictList.append(dictMaker(n,s,r,p))
        
    else:
        continue

with open('iofiles/rolls.json', "w") as object:
    json.dump(dictList, object, indent=2)

driver.close()
