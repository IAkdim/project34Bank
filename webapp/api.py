import paramiko
import requests
import json
import configparser

# SBC has no built in wifi, not sure if I can connect directly to the network with a cable or at all so I'm doing it through SSH.

def post_balance(data):
    '''
    This function is used to check the balance on a specific account. 
    It reads the SSH details from a config file, opens an SSH connection, sends a POST request to a specific API, 
    then closes the SSH connection.

    Args:
        data: a dictionary containing the required data for the POST request.

    Returns:
        The JSON response from the API request.
    '''
    # Read SSH details from config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Fetch SSH connection details from the config
    ssh_host = config.get('SSH', 'host')
    ssh_port = config.getint('SSH', 'port')
    ssh_username = config.get('SSH', 'username')
    ssh_password = config.get('SSH', 'password')

    # Start SSH session
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

    # API request URL
    url = 'http://145.24.222.140:8080/api/balance'
    headers = {'Content-type': 'application/json'}

    # Send the POST request
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Close SSH connection after the request
    ssh.close()

    # Return the API response in JSON format
    return response


def post_withdraw(data):
    '''
    This function is used to withdraw a certain amount from a specific account. 
    It reads the SSH details from a config file, opens an SSH connection, sends a POST request to a specific API, 
    then closes the SSH connection.

    Args:
        data: a dictionary containing the required data for the POST request.

    Returns:
        The JSON response from the API request.
    '''
    # Read SSH details from config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Fetch SSH connection details from the config
    ssh_host = config.get('SSH', 'host')
    ssh_port = config.getint('SSH', 'port')
    ssh_username = config.get('SSH', 'username')
    ssh_password = config.get('SSH', 'password')

    # Start SSH session
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

    # API request URL
    url = 'http://145.24.222.140:8080/api/withdraw'
    headers = {'Content-type': 'application/json'}

    # Send the POST request
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Close SSH connection after the request
    ssh.close()

    # Return the API response in JSON format
    return response
