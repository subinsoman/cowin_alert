#!/usr/bin/env python3

import requests
import time
import smtplib
import sys
from datetime import datetime
import logging
from logging import config as logging_config


class SixdeeLogger:
    sixdeelogger = None

    def __init__(self):
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - [%(module)s:%(levelname)s] - %(message)s"
                },
                "root": {
                    "format": "ROOT - %(asctime)s - [%(module)s:%(levelname)s] - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default"
                },
                "root_console": {
                    "class": "logging.StreamHandler",
                    "formatter": "root"
                }
            },
            "loggers": {
                "app": {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    # Don't send it up my namespace for additional handling
                    "propagate": False
                }
            },
            "root": {
                "handlers": ["root_console"],
                "level": "DEBUG"
            }
        }
        logging_config.dictConfig(LOGGING_CONFIG)

    def getlogger(self, name):
        return logging.getLogger(name)


log = SixdeeLogger().getlogger(__name__)


class Config:
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    # faking chrome browser
    browser_header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}


class Alert:
    def post(self, center,session):
        log.info("Center available" + str(center['name']))
        self.mailsend(center,session)

    def mailsend(self, center, session):
        gmail_user = 'tosubins@gmail.com'
        gmail_password = 'trzmfrlxmppsufbo'

        sent_from = gmail_user
        to = ['rajureshma463@gmail.com','subin.soman@6dtech.co.in']
        cc=[]
        bcc=[]
        subject = 'OMG Vaccine @ '+  str(center['name'])
        body = 'Hey bro , \n\t\t name:' + str(center['name']) + '\n\t\t address :'+str(center['address'])+'\n\t\t pincode :'+str(center['pincode'])+'   having slot  '+str(session['available_capacity_dose1'])+' on ' + session['date']
        to = [to] + cc + bcc
        message = 'Subject: {}\n\n{}'.format(subject, body)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, message)
            server.close()
        except Exception as e:
            # Print any error messages to stdout
            log.error(e)

        log.info('Email sent!')

    def whats_app_send(self, center, session):
        pass


class Cowin:
    @staticmethod
    def call_url(self, district_id):
        try:
            response = requests.get(
                Config.url + '?district_id=' + district_id + '&date=' + datetime.today().strftime('%d-%m-%Y'),
                headers=Config.browser_header)
            if response.ok:
                centers = response.json()['centers']
                for i in range(len(centers)):
                    sessions = centers[i]['sessions']
                    for j in range(len(sessions)):
                        session = sessions[j]
                        if session['available_capacity_dose1'] > 0 and session['min_age_limit'] == 18:
                            Alert().post(centers[i], session)
                        else:
                            pass
            else:
                log.error(response)
        except Exception as e:
            log.error("Error calling url " + str(e))


if __name__ == "__main__":
    while True:
        Cowin().call_url("294")
        time.sleep(1 * 30)
