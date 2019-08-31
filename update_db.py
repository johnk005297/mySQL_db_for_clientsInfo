import requests
import json
import mysql.connector


def get_data():

    user = 'user@boardmaps.com' + '/token'
    pwd = '<token>'
    headers = {'content-type': 'application/json'}

    url = "https://company.zendesk.com/api/v2/organizations.json"

    list_data = list()
    response = requests.get(url, auth=(user, pwd), headers=headers)

    if response.status_code != 200:
        print("No connection")
        exit()
    
    my_data = response.json()
      
    for line in my_data['organizations']:
        if line['organization_fields']['current_client'] is True:            
            list_data.append(line["name"])
            list_data.append(line["organization_fields"]["9845641687984123"])
            list_data.append(line["organization_fields"]["current_client"])
            list_data.append(line["organization_fields"]["saas"])
            list_data.append(line["organization_fields"]["db_plan"])
            list_data.append(line["organization_fields"]["custom_localization"])
            list_data.append(line["organization_fields"]["custom_skin_for_ipad"])
            list_data.append(line["organization_fields"]["custom_server_version"])         
            list_data.append(line["id"])
    
    result_data = tuple(list_data[i : i+9] for i in range(0, len(list_data), 9))
    
    return result_data
        
        
def db_update_organizations(data):

    connection = mysql.connector.connect(
        host = 'localhost',
        port = '3306',
        database = 'clientinfo',
        user = 'root',
        password = 'root'
    )
    cursor = connection.cursor()

    if not connection.is_connected():
        print("No connection")
            
    count = 0
    for line in data:
        query = """ UPDATE organizations SET  name = %s, current_version = %s, status = %s, saas = %s, db_maintenance_plan = %s, 
                            custom_localization = %s, custom_skin_for_ipad = %s, custom_server_version = %s
                    WHERE zendesk_id = %s """
                
        cursor.execute(query, line)    
        connection.commit()    
        if cursor.rowcount == 1:
            count += 1

    print()
    print(str(count) + " record(s) affected")
    
    cursor.close()
    connection.close()
    
def get_query():

    connection = mysql.connector.connect(
        host = 'localhost',
        port = '3306',
        database = 'clientinfo',
        user = 'root',
        password = 'root'
    )

    cursor = connection.cursor()
    if not connection.is_connected():
        print("No connection")
    
    query = """ SELECT id, name, current_version, zendesk_id FROM organizations """

    cursor.execute(query)
    result = cursor.fetchall()
    print(result)


def main():    
    data = get_data()     
    db_update_organizations(data)
    #get_query()    

if __name__ == "__main__":
    main()