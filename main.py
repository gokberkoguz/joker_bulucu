from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import configparser
import ast

class JokerFinder:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('conf.ini')
        self.driver = webdriver.Chrome('C:\Python27\selenium_driver\chromedriver.exe')

        self.places= ast.literal_eval(self.config['SELECTED_LOCATIONS']['LOCATIONS'])
        self.url= 'https://www.yemeksepeti.com'
        self.username = self.config['USER']['USERNAME']
        self.password = self.config['USER']['PASSWORD']
        self.time_to_wait = int(self.config['DEFAULT']['TIME_TO_WAIT'])
        self.current_page= 0
        self._check_selected_locations()
        self._check_user_cred()
        self.pass_list=[]
    def _check_selected_locations(self):
        try:
            self.selected_location = ast.literal_eval(self.config['SELECTED_LOCATIONS']['SELECTED_LOCATION'])
        except:
            self.selected_location = ''
        if self.selected_location is '':
            user_input = input('Arama yapılacak bölgeyi yazınız: For ex: besiktas')
            locations = [i for i in self.places if user_input in i]
            self._update_config('SELECTED_LOCATIONS','SELECTED_LOCATION',str(locations))
            self.selected_location = locations

    def _check_user_cred(self):
        if self.username is '':
            user_input = input('Username: ')
            self._update_config('USER','USERNAME',user_input)

        if self.password is '':
            user_input = input('Password: ')
            self._update_config('USER', 'PASSWORD', user_input)

    def _update_config(self,system,variable,value):
        self.config.set(system,variable,value)
        with open("conf.ini", "w+") as configfile:
            self.config.write(configfile)

    def click_joker(self):
        '''
                #joker olan yere tıklıyor eğer 2 tane varsa baştakine tıklıyor o yüzden tıklama komutunu devredışı bıraktım
                # tikla=self.driver.find_element_by_xpath('//*[@id="cboxLoadedContent"]/div/div/div[2]/div[2]/a')
                #joker cıktıktan sonra en alt kısımda joker suresi görünüyor.Bu bilgiyi çekiyor


                #joker çıktıysa True oluyor ve if içine giriyor
                #sirketi bulmanın yolu
                #//*[@id="cboxLoadedContent"]/div/div/div[2]/div[2]/a[' SAYI + ']
                #//*[@id="cboxLoadedContent"]/div/div/div[2]/div[2]/a[SAYI]
                #şeklindeydi string olarak aldığımız ve en fazla 5 tane joker indirimi gördüğüm için
                #for içinde döndürdüm.Öneri olarak kaç tane joker geldiği bulunabilir.Ona göre yapılırsa hata alıp yazdırma
                #kısmı da için içinden çıkmış olur
        '''
        try:
            joker=self.driver.find_element_by_xpath('//*[@id="cboxContent"]')
            self.driver.find_element_by_css_selector('#colorbox')
            joker=True
        except Exception as e:
            print(e)
            joker =False

        if joker is True:
            #print("girdi")
            time.sleep(3)
            try:
                kalan_sure=self.driver.find_element_by_xpath('//*[@id="cboxLoadedContent"]/div/div/div[3]/p[2]/span[2]').text
            except:
                pass
            for i in range(5):
                try:
                    sirket_path='//*[@id="cboxLoadedContent"]/div/div/div[2]/div[2]/a[' + str(i+1) + ']'
                    sirket_ismi = self.driver.find_element_by_xpath(sirket_path).text
                    print(sirket_ismi)
                    print("kalan sure", kalan_sure)

                    if not sirket_ismi in self.pass_list:
                        user_permission = input('Joker Bulundu!! Gecmek istiyor musunuz? ')
                        emin_misiniz = input('emin_misiniz ? ')
                    self.pass_list.append(sirket_ismi)

                except:
                    #print("joker yok", self.places[self.current_page])
                    pass
            try:
                self.driver.find_element_by_xpath('//*[@id="cboxClose"]').click()
            except:
                pass

        else:
            pass
            #print("joker yok",self.places[self.current_page])



    def login(self):
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/a[28]').click()
        except Exception as e:
            pass
        username_field = self.driver.find_element_by_id('UserName')
        username_field.click()
        username_field.send_keys(self.username)
        password_field = self.driver.find_element_by_id('password')
        password_field.click()
        password_field.send_keys(self.password)
        self.driver.find_element_by_id('ys-fastlogin-button').click()

    def change_page(self):
        self.current_page = ((self.current_page +1) % len(self.selected_location))
        self.driver.get("https://www.yemeksepeti.com" + self.selected_location[self.current_page])

    def search(self):
        pass

    def _run(self):

        self.driver.get("https://www.yemeksepeti.com" + self.selected_location[self.current_page])

        self.login()

        again=True

        while again:

            time.sleep(3)

            self.click_joker()

            self.change_page()

            time.sleep(3)



JokerFinder()._run()
