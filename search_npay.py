import argparse
import requests
import urllib.parse
from xml.etree import ElementTree as ET
import json
import os
import sys

# API key from ENV
API_KEY = os.getenv('HIRA_OPENAPI_KEY')

def get_hira_data(endpoint, params):
    if not API_KEY:
        print("Error: HIRA_OPENAPI_KEY environment variable is not set. Please set it to your valid API key.")
        sys.exit(1)
        
    base_url = "http://apis.data.go.kr/B551182/nonPaymentDamtInfoService"
    url = f"{base_url}/{endpoint}"
    
    # We will build the query string manually to avoid URL encoding issues with the API key
    query_str = f"?serviceKey={API_KEY}"
    for k, v in params.items():
        query_str += f"&{k}={urllib.parse.quote(str(v))}"
    
    full_url = url + query_str
    
    try:
        response = requests.get(full_url, timeout=15)
        response.encoding = 'utf-8' # HIRA API is xml utf-8
        
        # Try returning JSON if requested, else parsing XML to dict
        if 'type=json' in full_url or params.get('type') == 'json':
            return response.json()
            
        root = ET.fromstring(response.text)
        
        body = root.find('.//body')
        if body is None:
            return {"error": "API returned error", "raw": response.text[:500]}
            
        items = body.findall('.//item')
        results = []
        for item in items:
            record = {}
            for child in item:
                record[child.tag] = child.text
            results.append(record)
            
        return {
            "totalCount": body.find('./totalCount').text if body.find('./totalCount') is not None else 0,
            "pageNo": body.find('./pageNo').text if body.find('./pageNo') is not None else 1,
            "items": results
        }
    except Exception as e:
        return {"error": str(e), "raw_response": response.text[:500] if 'response' in locals() else ""}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query HIRA Non-Payment API")
    parser.add_argument("endpoint", help="getNonPaymentItemCodeList or getNonPaymentItemHospList etc")
    parser.add_argument("--pageNo", default=1, help="Page number")
    parser.add_argument("--numOfRows", default=10, help="Number of rows")
    parser.add_argument("--itemCd", help="Item code")
    parser.add_argument("--npayCd", help="Non-payment code")
    parser.add_argument("--sgguCd", help="Sigungu code")
    parser.add_argument("--sidoCd", help="Sido code")
    parser.add_argument("--yadmNm", help="Hospital name")
    
    args = parser.parse_args()
    
    params = {
        "pageNo": args.pageNo,
        "numOfRows": args.numOfRows
    }
    
    if args.itemCd: params["itemCd"] = args.itemCd
    if args.npayCd: params["npayCd"] = args.npayCd
    if args.sgguCd: params["sgguCd"] = args.sgguCd
    if args.sidoCd: params["sidoCd"] = args.sidoCd
    if args.yadmNm: params["yadmNm"] = args.yadmNm

    data = get_hira_data(args.endpoint, params)
    print(json.dumps(data, indent=2, ensure_ascii=False))
