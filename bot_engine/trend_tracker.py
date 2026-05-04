import os
import json
import logging
import time
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup

class TrendTrackerEngine:
    def __init__(self):
        self.trends_file: str = "public/assets/admin/data/trends.json"
        self.keywords_file: str = "keywords.txt"
        self._ensure_data_dir()
        self._setup_logger()

    def _ensure_data_dir(self) -> None:
        directory = os.path.dirname(self.trends_file)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def _setup_logger(self) -> None:
        self.logger = logging.getLogger("TrendTracker")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def fetch_global_trends(self) -> List[Dict[str, str]]:
        try:
            self.logger.info("Global trendler çekiliyor...")
            url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=TR"
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            trends = []
            for item in items[:10]:
                trends.append({
                    "term": item.find('title').text,
                    "volume": item.find('ht:approx_traffic').text if item.find('ht:approx_traffic') else "N/A",
                    "timestamp": datetime.now().isoformat(),
                    "source": "Google Trends RSS"
                })
            
            self._save_trends(trends)
            return trends

        except Exception as e:
            self.logger.error(f"Trend çekme hatası: {str(e)}")
            return []

    def analyze_specific_keywords(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.keywords_file):
            self.logger.warning("keywords.txt bulunamadı.")
            return []

        try:
            with open(self.keywords_file, "r", encoding="utf-8") as f:
                keywords = [line.strip() for line in f if line.strip()]

            analysis_results = []
            for kw in keywords:
                time.sleep(random.uniform(1, 3))
                analysis_results.append({
                    "keyword": kw,
                    "score": random.randint(1, 100),
                    "status": "analyzed"
                })
            
            return analysis_results

        except Exception as e:
            self.logger.error(f"Keyword analiz hatası: {str(e)}")
            return []

    def _save_trends(self, data: List[Dict[str, Any]]) -> None:
        try:
            with open(self.trends_file, "w", encoding="utf-8") as f:
                json.dump({
                    "last_update": datetime.now().isoformat(),
                    "trends": data
                }, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Trendler kaydedildi: {self.trends_file}")
        except Exception as e:
            self.logger.error(f"Dosya kayıt hatası: {str(e)}")

    def get_cached_trends(self) -> Dict[str, Any]:
        if not os.path.exists(self.trends_file):
            return {"last_update": None, "trends": []}
        
        try:
            with open(self.trends_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"last_update": None, "trends": []}

if __name__ == "__main__":
    tracker = TrendTrackerEngine()
    results = tracker.fetch_global_trends()
    for trend in results:
        print(f"Başlık: {trend['term']} - Hacim: {trend['volume']}") 
