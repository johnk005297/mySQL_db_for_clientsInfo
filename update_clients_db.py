import requests
import json
import mysql.connector
import time


class zendesk:    
       
    user = 'login@domen' + '/token'
    pwd = 'token'
    headers = {'content-type': 'application/json'}    

    organizationsUrl = "https://company.zendesk.com/api/v2/organizations.json"
    ticketsUrl = "https://company.zendesk.com/api/v2/tickets.json"
    

    def getDataForOrganizations(self):
        
        list_data = list()
        response = requests.get(self.organizationsUrl, auth=(self.user, self.pwd), headers=self.headers)

        if response.status_code != 200:
            print("No connection")
            exit()
        
        row_data = response.json()
        
        for line in row_data['organizations']:                 
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
            
            
    def db_update_organizations(self, data):
       
        db_connection = mysql.connector.connect(
            host = 'localhost',
            port = '3306',
            database = 'clients',
            user = 'root',
            password = 'root'
        )
        cursor = db_connection.cursor()

        if not db_connection.is_connected():
            print("No connection")             

        ### ON DUPLICATE KEY VERSION ###

        query = """ INSERT INTO organizations (name, current_version, status, saas, db_maintenance_plan, custom_localization, custom_skin_for_ipad, custom_server_version, zendesk_id) 
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate key 
        update name = values(name), current_version = values(current_version), status = values(status), saas = values(saas), db_maintenance_plan = values(db_maintenance_plan),
        custom_localization = values(custom_localization), custom_skin_for_ipad = values(custom_skin_for_ipad), custom_server_version = values(custom_server_version), zendesk_id = values(zendesk_id) """

        
        cursor.executemany(query,data)
        db_connection.commit()    
        
        print()    
        print(cursor.rowcount, "record(s) affected to organizations!")

        cursor.close()
        db_connection.close()



    def getDataForTickets(self):
        
        dataTickets = list()        

        while self.ticketsUrl is not None:
            # Do the HTTP get request
            r = requests.get(self.ticketsUrl, auth=(self.user, self.pwd), headers=self.headers)

            # Check for HTTP codes other than 200
            if r.status_code != 200:
                print('Status:', r.status_code, 'Problem with the request. Exiting.')
                exit()

            # Decode the JSON response into a dictionary and use the data
            data = r.json()
            
            for line in data['tickets']:           
                dataTickets.append(line['id'])
                dataTickets.append(line["status"])
                dataTickets.append(line["subject"])
                dataTickets.append(line["type"])
                dataTickets.append(line["priority"])                
                dataTickets.append((line["description"]).strip())                             
                dataTickets.append(line["created_at"][:10])                                               
                dataTickets.append(line["updated_at"][:10])                
                dataTickets.append(line["fields"][3]["value"]) # TFS links            
                dataTickets.append(line["fields"][2]["value"]) # reason                
                dataTickets.append(line["organization_id"])
                dataTickets.append(line["requester_id"])           
                dataTickets.append(line['assignee_id'])
                dataTickets.append(line["group_id"]) 
                
            self.ticketsUrl = data["next_page"]                
                
            final_data = tuple(dataTickets[i : i+14] for i in range(0, len(dataTickets), 14))            
                
        return final_data

    def db_update_tickets(self, data):

        db_connection = mysql.connector.connect(
            host = 'localhost',
            port = '3306',
            database = 'clients',
            user = 'root',
            password = 'root'
        )     
        cursor = db_connection.cursor()

        if not db_connection.is_connected():
            print("No connection")  
        

        ### ON DUPLICATE KEY VERSION ###
            
        query = """ INSERT INTO tickets (id, status, subject, type, priority, description, created_at, updated_at, tfs, reason, zendesk_org_id,
        requester_id, assignee_id, group_id)         
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        ON duplicate KEY UPDATE     
        status = values(status), subject = values(subject), type = values(type), priority = values(priority), description = values(description),
        created_at = values(created_at), updated_at = values(updated_at), tfs = values(tfs), reason = values(reason), zendesk_org_id = values(zendesk_org_id),
        requester_id = values(requester_id) , assignee_id = values(assignee_id), group_id = values(group_id)
        """

        
        cursor.executemany(query, data)
        db_connection.commit()    
        
        print()    
        print(cursor.rowcount, "record(s) affected to tickets!")

        cursor.close()
        db_connection.close()


    def main(self):
        z = zendesk()
        start = time.time()        
        z.db_update_organizations(z.getDataForOrganizations())
        z.db_update_tickets(z.getDataForTickets())     
        end = time.time()
        print("execution time: " + str(round(end - start, 3)) + " seconds")

if __name__ == "__main__":
    zendesk().main()
