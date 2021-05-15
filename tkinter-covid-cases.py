import tkinter as tk
import http.client
import json

root = tk.Tk()
root.title('Tkinter Covid Cases')
root.minsize(400,500) == root.maxsize(400,500)
root.configure(background='#A7BBC7')
canvas = tk.Canvas(root, height=500, width=400, bg='#A7BBC7', highlightthickness=0).pack()


placeHolderDeleted = False
def clear_placeholder(self):
    global placeHolderDeleted
    if placeHolderDeleted == False:
        inputBar.delete("1.0","end-1c")
        placeHolderDeleted = (True)
    else:
        return

def get_data_from_api(self):
    global listData
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type':"application/json",
        'authorization':"apikey <your_api_key>"}           # API key taken from collectapi.com
    conn.request("GET", "/corona/countriesData", headers=headers)
    res = conn.getresponse()
    data = res.read()
    strData = data.decode("utf-8")
    dictData = json.loads(strData)
    listData = dictData['result']
    return listData


def get_input(self):
    global inputCountry
    countries = []
    for x in listData:
        newCountry = x['country']
        countries.append(newCountry)

    firstInput = str(inputBar.get("1.0","end-1c"))
    if firstInput.lower() in [element.lower() for element in countries]:
        inputCountry = firstInput
        print(inputCountry)
        inputBar.delete("1.0","end-1c")
        return True
    else:
        inputBar.delete("1.0","end-1c")
        return False
    
   
def check_country(self):
    i = 0
    global countryFile
    for item in listData:
        if item['country'].lower() == inputCountry.lower():
            countryFile = listData[i]
        i += 1


def display_data(self):
    print(countryFile)
    lst = [('Country: ', countryFile['country']),
            ('Total Cases: ', countryFile['totalCases']),
            ('New Cases: ', countryFile['newCases']),
            ('Total Deaths: ', countryFile['totalDeaths']),
            ('New Deaths: ', countryFile['newDeaths']),
            ('Total Recovered: ', countryFile['totalRecovered']),
            ('Active Cases: ', countryFile['activeCases'])]
    newWindow = tk.Toplevel(root)
    newWindow.title('COVID-19 Status in ' + countryFile['country'])
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            table = tk.Entry(newWindow, width=30)
            table.grid(row=i, column=j)
            table.insert('end', lst[i][j])
    

def main():
    get_data_from_api('self')
    if get_input('self') == True:
        check_country('self')
        display_data('self')
    elif get_input('self') == False:
        errorWindow = tk.Toplevel(root)
        errorWindow.title('ERROR - No such country!')
        errorSign = tk.Label(errorWindow, text="Seems like you've made a typo.\n Please try again...", width=50)
        errorSign.pack()
        return


covidLogo = tk.PhotoImage(file='<image_path>')    # Path of covid image.
logoLabel = tk.Label(root, image=covidLogo, bg='#A7BBC7').place(relx=0.5, rely=0.15, anchor='n')

inputBar = tk.Text(root, height=0.2, width=30)
inputBar.place(relx=0.5, rely=0.6, anchor='n')

inputBar.bind('<Button-1>', clear_placeholder)

actionButton = tk.Button(root, text='Get Cases', height=1, width=10,
                bg='#515BD4', relief='ridge', font=('Helvetica', 10),
                command=lambda: main())
actionButton.place(relx=0.5, rely=0.7, anchor='n')
inputBar.insert('end', 'Enter a country...')

catchPhrase = tk.Label(root, text='Up to date Covid19 cases from anywhere...', bg='#A7BBC7').place(relx=0.5, rely=0.85, anchor='n')

root.mainloop()