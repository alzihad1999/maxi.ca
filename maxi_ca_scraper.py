import requests
import json

# Headers for the HTTP request
headers = {
    'Accept': '*/*',
    'Accept-Language': 'fr',
    'Business-User-Agent': 'PCXWEB',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://www.maxi.ca',
    'Origin_Session_Header': 'B',
    'Referer': 'https://www.maxi.ca/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'is-helios-account': 'false',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
    'x-application-type': 'Web',
    'x-channel': 'web',
    'x-loblaw-tenant-id': 'ONLINE_GROCERIES',
    'x-preview': 'false',
}

# Template for JSON data in the POST request
json_data_template = {
    'cart': {'cartId': 'f69b6e5a-75c2-446a-ba0e-80d2ab12ea3d'},
    'fulfillmentInfo': {
        'storeId': '7568',
        'pickupType': 'STORE',
        'offerType': 'OG',
        'date': '06072024',
        'timeSlot': None,
    },
    'listingInfo': {
        'filters': {},
        'sort': {},
        'pagination': {'from': 1},
        'includeFiltersInResponse': True,
    },
    'banner': 'maxi',
    'userData': {
        'domainUserId': 'f1158223-97d8-45b3-977d-e7ee815c088b',
        'sessionId': '46caa27c-cc3a-4ba8-8615-807d73ee6d97',
    },
}

# List of category codes to fetch data for
code_list = [
    '28039', '28040', '28043', '28038', '58045', '58466', '58498', '58556', '58561', '58680', 
    '58801', '58812', '58873', '28180', '28181', '28175', '28303', '28304', '28305', '28306', 
    '59461', '28146', '57029', '41118', '28182', '39932', '28228', '28229', '28230', '28231', 
    '28232', '28233', '28234', '28235', '29718', '59462', '28147', '28148', '28149', '28150', 
    '28251', '59494', '28030', '28031', '28035', '28025', '28028', '28032', '28026', '28029', 
    '28033', '28034', '42410', '28480', '28158', '28201', '28202', '28203', '28204', '28212', 
    '57039', '28194', '28195', '28196', '28197', '28198', '28199', '28200', '59222', '28183', 
    '28184', '28185', '28186', '28187', '28188', '28243', '28244', '28245', '28246', '28247', 
    '28248', '57088', '28242', '28249', '28250', '59210', '28009', '28010', '28014', '28018', 
    '28021', '28015', '28016', '28019', '28008', '28013', '28017', '56939', '56859', '39716', 
    '29713', '29714', '29717', '29924', '29925', '29927', '59260', '59271', '59281', '59302', 
    '59320', '59339', '59374', '59391', '28190', '28191', '28192', '28193', '28217', '28218', 
    '28219', '28220', '28221', '28222', '28223', '28224', '28225', '28226', '28227', '58904', 
    '59463', '28162', '28163', '28164', '28165', '28238', '28239', '28240', '28241', '57003', 
    '59459', '28166', '28167', '28168', '28169', '28205', '28206', '28207', '28208', '28209', 
    '28210', '28211', '57043', '28129', '28132', '28133', '28127', '28128', '28131', '28134', 
    '59460', '28170', '28171', '28173', '28174', '28214', '28215', '28216', '59252', '59253', 
    '59257', '59318', '59319'
]

data = []

print(f"Total category codes: {len(code_list)}")

# Loop over each category code and fetch data
for index, code in enumerate(set(code_list)):
    print(f"Processing code {index + 1}/{len(code_list)}: {code}")
    page_number = 1
    
    while True:
        # Update pagination in the JSON data
        json_data_template['listingInfo']['pagination']['from'] = page_number

        # Make the POST request
        response = requests.post(
            f'https://api.pcexpress.ca/pcx-bff/api/v2/listingPage/{code}',
            headers=headers,
            json=json_data_template
        )
        
        try:
            # Try to get product data from the main content section
            results = response.json()['layout']['sections']['mainContentCollection']['components'][0]['data']['productTiles']
        except KeyError:
            try:
                # Fallback to another section if main content is not available
                results = response.json()['layout']['sections']['productListingSection']['components'][0]['data']['productGrid']['productTiles']
            except KeyError:
                break

        if not results:
            break

        # Append results to data list
        data.extend(results)
        page_number += 1

# Save the extracted data to a JSON file
with open('maxi_ca.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Task Completed.")
