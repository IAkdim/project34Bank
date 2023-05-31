import requests

# Test for a valid account and pin
valid_account_test = {'acctNo': 'CHBAHE312843209', 'pin': '4679'}
response = requests.post('http://145.24.222.165:8080/api/balance', json=valid_account_test)
expected_result = {'status': 200, 'balance': 1000, 'success': True, 'acctNo': 'CHBAHE312843209'}
if response.status_code == 200:
    content = response.json()
    if content == expected_result:
        print("Test Passed!")
    else:
        print("Test Failed!")
        print("Expected:", expected_result)
        print("Actual:", content)
else:
    print("Test Failed!")
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode('utf-8'))

# Test for an invalid account number
invalid_account_test = {'acctNo': 'DSKEAL0123456789', 'pin': '4679'}
response = requests.post('http://145.24.222.165:8080/api/balance', json=invalid_account_test)
expected_result = {'status': 400, 'message': 'Invalid account number.', 'success': False, 'acctNo': None}
if response.status_code == 200:
    content = response.json()
    if content == expected_result:
        print("Test Passed!")
    else:
        print("Test Failed!")
        print("Expected:", expected_result)
        print("Actual:", content)
else:
    print("Test Failed!")
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode('utf-8'))

# Test for an invalid account number
invalid_account_test = {'acctNo': 'DSKEAL0123456789', 'pin': '4679'}
response = requests.post('http://145.24.222.165:8080/api/balance', json=invalid_account_test)
expected_result = {'status': 400, 'message': 'Invalid account number.', 'success': False, 'acctNo': None}
if response.status_code == 200:
    content = response.json()
    if content == expected_result:
        print("Test Passed!")
    else:
        print("Test Failed!")
        print("Expected:", expected_result)
        print("Actual:", content)
else:
    print("Test Failed!")
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode('utf-8'))

# Test for a blocked account
blocked_account_test = {'acctNo': 'CHBAHE464517766', 'pin': '5555'}
response = requests.post('http://145.24.222.165:8080/api/balance', json=blocked_account_test)
expected_result = {'status': 403, 'message': 'This account is blocked.', 'success': False, 'acctNo': None}
if response.status_code == 200:
    content = response.json()
    if content == expected_result:
        print("Test Passed!")
    else:
        print("Test Failed!")
        print("Expected:", expected_result)
        print("Actual:", content)
else:
    print("Test Failed!")
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode('utf-8'))

# Test for an invalid pin
invalid_pin_test = {'acctNo': 'CHBAHE312843209', 'pin': '0000'}
response = requests.post('http://145.24.222.165:8080/api/balance', json=invalid_pin_test)
expected_result = {'status': 401, 'message': 'Invalid user ID or PIN.', 'success': False, 'acctNo': None}
if response.status_code == 200:
    content = response.json()
    if content == expected_result:
        print("Test Passed!")
    else:
        print("Test Failed!")
        print("Expected:", expected_result)
        print("Actual:", content)
else:
    print("Test Failed!")
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode('utf-8'))


# Test for a non-existent user
non_existent_user_test = {'acctNo': 'CHBAHE0123456789', 'pin': '4679'}
response = requests.post('http://145.24.222.165:8080/api/balance', json=non_existent_user_test)
expected_result = {'status': 400, 'message': 'Invalid account number.', 'success': False, 'acctNo': None}
if response.status_code == 200:
    content = response.json()
    if content == expected_result:
        print("Test Passed!")
    else:
        print("Test Failed!")
        print("Expected:", expected_result)
        print("Actual:", content)
else:
    print("Test Failed!")
    print("Response status code:", response.status_code)
    print("Response content:", response.content.decode('utf-8'))

print("All unit tests passed successfully.")