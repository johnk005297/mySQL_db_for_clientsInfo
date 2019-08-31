import json
import mysql.connector
import requests



def get_organization_data():
    
    user = 'user@boardmaps.com' + '/token'
    pwd = '<token>'
    headers = {'content-type': 'application/json'}

    url = "https://company.zendesk.com/api/v2/organizations.json"

    list_data = list()

    # Do the HTTP get request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()

    print()
    ### Getting data from zendesk about clients ###
    for line in data["organizations"]:
        if line["organization_fields"]["current_client"] is True:
            list_data.append(line["name"])
            list_data.append(line["organization_fields"]["9845641687984123"])
            list_data.append(line["organization_fields"]["current_client"])
            list_data.append(line["organization_fields"]["saas"])
            list_data.append(line["organization_fields"]["custom_localization"])
            list_data.append(line["organization_fields"]["custom_server_version"])
            list_data.append(line["organization_fields"]["custom_skin_for_ipad"])
            list_data.append(line["organization_fields"]["db_plan"])
            list_data.append(line["id"])
    
    clients_data = tuple(list_data[i : i+9] for i in range(0, len(list_data), 9))
    return clients_data
    

def insert_dataInto_db():
    mydb = mysql.connector.connect(
        host='localhost',
        port='3306',
        database='clientinfo',
        user='root',
        password='root' )

        
    db_query = mydb.cursor()
    if not mydb.is_connected():
        print("No connection with the db!")
    
    add_org = """ INSERT IGNORE INTO organizations (name, current_version, status, saas, custom_localization, custom_server_version, custom_skin_for_ipad, db_maintenance_plan, zendesk_id) 
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
    client_info = get_organization_data()

    db_query.executemany(add_org, client_info)
    mydb.commit()
    
    print(db_query.rowcount, "record(s) affected")
       
    db_query.close()
    mydb.close()
    

def main():
    get_organization_data()
    insert_dataInto_db()

if __name__ == "__main__":
    main()
    
