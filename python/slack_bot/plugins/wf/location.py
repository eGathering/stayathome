#!/usr/bin/python3
"""
地名を管理するためのモジュール
"""
import re
from urllib import request
from urllib.error import URLError
import xml.etree.ElementTree as ET

class _City():
    """ 都市の情報を保持するクラス """
    def __init__(self, name, id):
        self._name = name
        self._id = id

    def name(self):
        """ 都市の名前を取得する """
        return self._name

    def id(self):
        """ 都市のidを取得する """
        return self._id

class _Prefecture(dict):
    """ 都道府県の情報を保持するクラス """
    def __init__(self, name):
        self._name = re.sub(r'[都府県]', '', name)
        self._capital = None

    def regCapital(self, city):
        """ 都道府県庁所在地を登録する """
        self._capital = city

    def name(self):
        """ 都道府県の名前を取得する """
        return self._name

    def capital(self):
        """ 都道府県庁所在地を取得する """
        return self._capital

class Location(dict):
    """
    各観測場所の情報を管理するテーブル。
    シングルトン。
    """
    _instance = None
    _xmlurl = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'

    def _getXmlData(self):
        req = request.Request(self._xmlurl)
        with request.urlopen(req) as response:
            xmldata = response.read()
        return xmldata

    def __new__(cls):
        if cls._instance:
            return cls._instance

        self = dict.__new__(cls)
        cls._instance = self
        return self

    def __init__(self):
        try:
            root = ET.fromstring(self._getXmlData())
        except URLError as e:
            self._instance = None
            raise

        for prefnode in root.iter('pref'):
            pref = _Prefecture(prefnode.get('title'))
            for citynode in prefnode.findall('city'):
                city = _City(citynode.get('title'), citynode.get('id'))
                pref[city.name()] = city
                if not pref.capital():
                    pref.regCapital(city)
            self[pref.name()] = pref

    def findId(self, name):
        """
        名前に対応するIDと都市名を返す。
        見つからない場合は、Noneを返す。
        """
        # 北海道だけ自治体単位でないため、ここで変換
        name = re.sub('北海道', '道北', name)
        if name in self:
            return self[name].capital().id()
        for pref in self.values():
            if name in pref:
                return pref[name].id()
        return None

    def getAvailablePrefs(self):
        """ 利用可能な都道府県の名前を返す """
        names = list()
        for name in self:
            names.append(name)
        # 北海道だけ自治体単位でないため、ここで追加
        names.append('北海道')
        return set(names)

    def getAvailableCities(self):
        """ 利用可能な都市の名前を返す """
        names = list()
        for pref in self.values():
            for name in pref:
                names.append(name)
        return set(names)

    def getAvailableNames(self):
        """ 利用可能な全名前を返す """
        prefs = self.getAvailablePrefs()
        cities = self.getAvailableCities()
        return prefs | cities

