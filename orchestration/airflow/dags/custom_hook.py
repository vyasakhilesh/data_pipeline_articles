from airflow.hooks.base_hook import BaseHook
import requests

class CustomAPIHook(BaseHook):
    def __init__(self, conn_id):
        super().__init__()
        self.conn_id = conn_id
        self.conn = self.get_connection(conn_id)
        
    def get_conn(self):
        return requests.Session()

    def get_data(self, endpoint):
        session = self.get_conn()
        response = session.get(f"{self.conn.host}/{endpoint}", headers={"Authorization": f"Bearer {self.conn.password}"})
        response.raise_for_status()
        return response.json()
    
    def write_data(self, data, endpoint):
        session = self.get_conn()
        response = session.post(f"{self.conn.host}/{endpoint}", json=data, headers={"Authorization": f"Bearer {self.conn.password}"})
        response.raise_for_status()
        return response.json()
