import requests 
import pandas as pd 
from datetime import datetime
import time
import io  

def crawl_and_append_csv(url, combined_df):
    res = requests.get(url)
    data_csv = pd.read_csv(io.StringIO(res.content.decode('utf-8')))
    
    combined_df = pd.concat([combined_df, data_csv], ignore_index=True)
    
    return combined_df, data_csv  
def date_range(start_date, end_date, url_template, api_key, limit, output_path):
    start_date_str = datetime.strptime(start_date, "%Y/%m/%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
    end_date_str = datetime.strptime(end_date, "%Y/%m/%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
    
    combined_df = pd.DataFrame() 
    
    offset = 0
    while True:
        url = url_template.format(start_date_str, end_date_str, api_key, offset, limit)
        combined_df, data_csv = crawl_and_append_csv(url, combined_df)
        
        # 如果新獲取的資料筆數為 0 或最晚日期超過指定範圍，則停止
        if data_csv.empty or data_csv['publishtime'].max() > end_date_str:
            break
        
        # 更新 offset
        offset += limit
        time.sleep(1)  
    
    # 將結果儲存為 CSV
    combined_df.to_csv(output_path, index=False, encoding='utf-8')

start_date = "2024/08/12 00:00:00"
end_date = "2024/08/12 19:00:00"
api_key = "b7debcc9-0a9d-41c2-bace-f649afad257c"
limit = 1000
output_path = "D:/mushroom/research/air/2024/0318_0324/test_Air.csv"
url_template = "https://data.moenv.gov.tw/api/v2/aqx_p_432?format=csv&filters=publishtime,GR,{0}|publishtime,LE,{1}&api_key={2}&offset={3}&limit={4}"

date_range(start_date, end_date, url_template, api_key, limit, output_path)
