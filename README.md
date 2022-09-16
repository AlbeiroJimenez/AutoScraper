# AutoScraper
#AutoScrapper is designed to do crawling of information about used cards in some markeplace as Facebook, Kavak, #OlxAutos, and so on...

#Use Instructions Facebook Crawler

#1. Run crawler.py module in a terminal or IDLE of your preference.
#2. Login in Facebook throughout Selenium Marionette with the command:
       facebook.loginFacebook()
#3. Set the marketplace epicenter (Lima, Trujillo, south of Peru) with the command:
       facebook.spyder.setDriver(facebook.urlMarket[0])  where 0-Lima, 1-Trujillo and 2-South of Peru.
#4. Scroll the selenium marionette until you get the desired number of ads.
#5. Run the crawling with the command:
       facebook.makeCrawling_threaded('NameDatabase.xlsx', epicenterNumber) 
       Where: 
           NameDatabase - Name assigned to the database
           epicenterNumber: 0-Lima, 1-Trujillo, 2-South of Peru.
#6. If you want to stop the process in the idle, run the command:
       facebook.stop=True
#7. When the process finish run the following commands:
       dataToSave = pd.DataFrame(facebook.database)
       dataToSave.to_excel(NameDatabase.xlsx)
#8. Enjoy crawling with AutoScraper! 

#Use Instructions Kavak Crawler

#1. Run crawler.py module in a terminal or IDLE of your preference.
#2. Run the crawling with the command:
       facebook.makeCrawling()
#3. Making the Kavak Database with the command:
       kavak.getBaseKavak()
#4. Enjoy crawling with AutoScraper!


