import pandas as pd
import instagram_thread
import time
import threading
import Process

class myThread(threading.Thread):
    def __init__(self,headers,number,List):
        threading.Thread.__init__(self)
        self.headers = headers
        self.number = number
        self.List = List
    def run(self):
        print("开始线程"+str(self.number))
        getFeature(self.headers,self.number,self.List)
        print("结束线程"+str(self.number))        

def getFeature(headers,number,List):
    myrange = len(List)//5
    if(myrange==0):
        if(number==1):
            for i in range(0,len(List)):
                instagram_thread.main(str(List[i]),headers,number)
                time.sleep(10)
        else:
            pass
    else:
        if(number!=5):
            for i in range((number-1)*myrange,number*myrange):
                instagram_thread.main(str(List[i]),headers,number)
                time.sleep(10)
        else:
            for i in range((number-1)*myrange,len(List)):
                instagram_thread.main(str(List[i]),headers,number)
                time.sleep(10)



def runThread(length,List,which):
    headers1 = {
        'authority': 'www.instagram.com',
        'method': 'GET',
        'path': '/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%221507979106%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D',
        'scheme': 'https',
        'cookie': 'ig_did=22291BA2-9977-490C-AD8F-77A545179274; ig_nrcb=1; mid=YHzigAALAAHQHRdBBPtschF7FrI5; datr=RKmbYFUJAadmRXOsfon0kDpt; ds_user_id=47793281340; sessionid=47793281340%3AguIQJ9uNbBZRZc%3A18; csrftoken=p1t3NmYWzv1xAH7CZRiJnJdhsdm5LaPf; rur=VLL',
        'referer': 'https://www.instagram.com/skuukzky/followers/?hl=zh-cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'x-csrftoken': 'p1t3NmYWzv1xAH7CZRiJnJdhsdm5LaPf',
        'x-ig-app-id':'936619743392459',
        'x-ig-www-claim': 'hmac.AR3V7UCz6lgFvceWfBVhf56H6X-vlEwCO2Etg6nC_TZdZq8u',
        'x-requested-with': 'XMLHttpRequest',
    }

    headers2 = {
        'authority': 'www.instagram.com',
        'method': 'GET',
        'path': '/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%221507979106%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D',
        'scheme': 'https',
        'cookie': 'mid=YJFHHQALAAFKWNuESKiRDTHzlrKG; ig_did=B5CAB298-E044-4292-9357-F75C3C4F125A; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; ds_user_id=47793281340; sessionid=47793281340%3AyVcUIdqKanualA%3A2; csrftoken=7ZM7UcYxaJLyTwdPI4WfZLuyeR8YAKia; rur=VLL',
        'referer': 'https://www.instagram.com/skuukzky/followers/?hl=zh-cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'x-csrftoken': '7ZM7UcYxaJLyTwdPI4WfZLuyeR8YAKia',
        'x-ig-app-id':'936619743392459',
        'x-ig-www-claim': 'hmac.AR3V7UCz6lgFvceWfBVhf56H6X-vlEwCO2Etg6nC_TZdZoL2',
        'x-requested-with': 'XMLHttpRequest',
    }

    headers3 = {
        'authority': 'www.instagram.com',
        'method': 'GET',
        'path': '/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%221507979106%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D',
        'scheme': 'https',
        'cookie': 'mid=YJFHHQALAAFKWNuESKiRDTHzlrKG; ig_did=B5CAB298-E044-4292-9357-F75C3C4F125A; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; ds_user_id=47793281340; sessionid=47793281340%3AyVcUIdqKanualA%3A2; csrftoken=7ZM7UcYxaJLyTwdPI4WfZLuyeR8YAKia; rur=VLL',
        'referer': 'https://www.instagram.com/skuukzky/followers/?hl=zh-cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'x-csrftoken': '7ZM7UcYxaJLyTwdPI4WfZLuyeR8YAKia',
        'x-ig-app-id':'936619743392459',
        'x-ig-www-claim': 'hmac.AR3b0kCjXyO60g_v9Rta-K_LGe-jvEqsaXBTPTtAtDyEzJ2G',
        'x-requested-with': 'XMLHttpRequest',
    }

    headers4 = {
        'authority': 'www.instagram.com',
        'method': 'GET',
        'path': '/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%221507979106%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D',
        'scheme': 'https',
        'cookie': 'ig_did=22291BA2-9977-490C-AD8F-77A545179274; ig_nrcb=1; mid=YHzigAALAAHQHRdBBPtschF7FrI5; ds_user_id=47672457035; sessionid=47672457035%3AJVGTOJOF38wskt%3A0; csrftoken=6C1vLEWwCEJGgVu8snw5jnNXkqCM7hcQ; rur=ASH',
        'referer': 'https://www.instagram.com/skuukzky/followers/?hl=zh-cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'x-csrftoken': '6C1vLEWwCEJGgVu8snw5jnNXkqCM7hcQ',
        'x-ig-app-id':'936619743392459',
        'x-ig-www-claim': 'hmac.AR3b0kCjXyO60g_v9Rta-K_LGe-jvEqsaXBTPTtAtDyEzJtG',
        'x-requested-with': 'XMLHttpRequest',
    }

    headers5 = {
        'authority': 'www.instagram.com',
        'method': 'GET',
        'path': '/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%221507979106%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D',
        'scheme': 'https',
        'cookie': 'ig_did=22291BA2-9977-490C-AD8F-77A545179274; ig_nrcb=1; mid=YHzigAALAAHQHRdBBPtschF7FrI5; ds_user_id=47485569903; sessionid=47485569903%3A3DaEXGCEWafA1W%3A11; csrftoken=eJ5tTpo3VDDJBq76bSDnDotYt8viBV9y; rur=RVA',
        'referer': 'https://www.instagram.com/skuukzky/followers/?hl=zh-cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'x-csrftoken': 'eJ5tTpo3VDDJBq76bSDnDotYt8viBV9y',
        'x-ig-app-id':'936619743392459',
        'x-ig-www-claim': 'hmac.AR05IzkG46dhT5HH33pv8SBsgezyeOMOvoefm0JZvIFWG4bz',
        'x-requested-with': 'XMLHttpRequest',
    }
    if(len(List)!=0):
        thread1 = myThread(headers1,1,List)
        # thread2 = myThread(headers2,2,List)
        # thread3 = myThread(headers3,3,List)
        # thread4 = myThread(headers4,4,List)
        # thread5 = myThread(headers5,5,List)

        thread1.start()
        # thread2.start()
        # thread3.start()
        # thread4.start()
        # thread5.start()

        thread1.join()
        # thread2.join()
        # thread3.join()
        # thread4.join()
        # thread5.join()

        if(which==0):
            pass
        else:
            Process.process(1)
            # Process.process(2)
            # Process.process(3)
            # Process.process(4)
            # Process.process(5)
    else:
        pass