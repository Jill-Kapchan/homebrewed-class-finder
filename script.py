import requests
from twilio.rest import Client
from bs4 import BeautifulSoup, Comment

#Example scraped data indexes
#Index     Data
#0)        CSE 511
#1)        Data Processing at Scale
#2)        85574
#3)        Ghayekhloo
#4)        M W
#5)        1:30 PM
#6)        2:45 PM
#10)       ['72', '120']

#Make sure to put the class number
classesToNotify = ['CLASS_LIST']

def sendText(classInfo):
    #API information
    account_sid = SID
    auth_token = TOKEN
    client = Client(account_sid, auth_token)
    
    textBody = "The following class has opened up:\n" + classInfo + "\nhttps://webapp4.asu.edu/myasu/"
    
    message = client.messages.create \
                (
                    body = textBody,
                    from_= TWILIO_NUMBER,
                    to = PERSONAL_NUMBER
                )
    return None
    
def main():
    #Dictionary will have key:value of class#:open seats
    #If the number of open seats increases by at least one, 
    #then the code will send a text notification
    dic = {}

    #AJAX url for the request sent by the website
    url = "https://webapp4.asu.edu/catalog/myclasslistresults?t=2217&s=CSE&n=5*&hon=F&promod=F&e=open&page=1"
    
    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
   
        #Removes all the HTML comments for easier parsing
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()
        #print(soup.prettify())

        #Find the table and each of the rows
        table = soup.find('tbody')
        rows = table.findAll('tr')

        for r in rows:
            column = r.findAll('td')
            classInfo = ""
    
            for i in [0,1,2,3,4,5,6,10]:
                if i == 5:
                    classInfo += column[i].text.strip() + "-"
                #index 10 has a string with new lines and white space
                elif i == 10:
                    oneLine = column[i].text
                    formattedSize = list(oneLine.split('\n'))
            
                    #index0 -> open seats
                    #index1 -> total seats
                    openSeats = []
                    openSeats.append(formattedSize[4])
                    openSeats.append(formattedSize[9])
                    #print(openSeats)
                
                    #Check if the class number is saved in the dictionary
                    classNumber = column[2].text.strip()
                    if classNumber not in dic.keys():
                        dic[classNumber] = (openSeats[0])
                    else:
                        prevNumOpenSeats =  dic[classNumber]
                        currNumOpenSeats = openSeats[0]
                    
                        #More currNumOpenSeats means a seat opened up
                        #Send notification to user
                        if currNumOpenSeats > prevNumOpenSeats:
                            classInfo.strip()
                            sendText(classInfo)

                        dic[classNumber] = currNumOpenSeats
                else:
                    classInfo += column[i].text.strip() + " "
    
if __name__== "__main__":
    main()