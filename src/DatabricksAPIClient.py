import subprocess
import sys
import json
import base64
import os
import requests
import uuid
from copy import deepcopy
from databricks_cli.sdk import ApiClient

from .sdk.BetterLibrariesService import BetterLibrariesService

class DatabricksAPIClient:
  def __init__(self, host:str, token:str):
    self.api_client = ApiClient(host=host, token=token)
    #self.jobs_service = JobsService(self.api_client)
    #self.runs_api = RunsApi(self.api_client)
    #self.cluster_service = BetterClusterService(self.api_client)
    #self.secret_service = BetterSecretService(self.api_client)
    #self.workspace_service = WorkspaceService(self.api_client)
    self.libraries_service = BetterLibrariesService(self.api_client)
    #self.group_service = GroupsService(self.api_client)
    #self.scim_service = BetterSCIMService(self.api_client)
    #self.dbfs_service = BetterDbfsService(self.api_client)
    
  @classmethod
  def _get_notebook_context(cls, dbutils):
    return json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())
  
  @classmethod
  def from_notebook_context(cls, dbutils):
    ctx = cls._get_notebook_context(dbutils)
    api_host = 'https://' + ctx['tags']['browserHostName']
    api_token = ctx['extraContext']['api_token']
    
    return DatabricksAPIClient(api_host, api_token)
  
  @classmethod
  def _get_az_aad_token_interactive(cls, tenant_id):
    process = subprocess.Popen(
      ["az", "login", "--tenant", tenant_id], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    for line in process.stdout:
      print(line.decode('utf-8'), end='')
      
    p = subprocess.run(["az", "account", "get-access-token", "--resource", "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d"], capture_output=True, text=True)
    az_access_token_json = p.stdout
    az_access_token = json.loads(az_access_token_json)
    return az_access_token['accessToken']
  
  @classmethod
  def from_azure_interactive_login(cls, tenant_id, api_host=None):
    az_access_token = cls._get_az_aad_token_interactive(tenant_id)
    ctx = cls._get_notebook_context()
    api_host = api_host or ('https://' + ctx['tags']['browserHostName'])
    
    return DatabricksAPIClient(api_host, az_access_token)
  
  @classmethod
  def from_token(cls, host, token):
    return DatabricksAPIClient(host, token)