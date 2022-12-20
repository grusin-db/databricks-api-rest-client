import json
from databricks_cli.sdk import ApiClient
from databricks_cli.libraries.api import LibrariesApi

class BetterLibrariesService(LibrariesApi):
  def __init__(self, client:ApiClient):
    super().__init__(client)

  def get_cluster_libraries(self, cluster_id: str) -> dict:
    """gets installed libraries on a cluster

    Args:
			cluster_id (str): cluster id string

    Returns:
			dict: installed libraries on a cluster, per dbr api results
    """

    return [ 
      x['library'] 
      for x in self.cluster_status(cluster_id).get('library_statuses', []) 
    ]
    
  @classmethod
  def get_libraries_diff(cls, src_libs:list[dict], target_libs:list[dict]) -> dict:
    """compares source and destination libraries and generated libraries that needs installing or removing 

    Args:
			src_libs (list[dict]): list of installed libraries returned from `.get_cluster_libraries(...)`
			target_libs (list[dict]): list of installed libraries returned from `.get_cluster_libraries(...)`

    Returns:
			dict: dictionary containing 'to_remove' and 'to_install' libraries defintion
    """
    x_src_libs = [json.dumps(x) for x in src_libs]
    x_target_libs = [json.dumps(x) for x in target_libs]

    to_install = [json.loads(x) for x in (set(x_src_libs) - set(x_target_libs))]
    to_remove = [json.loads(x) for x in (set(x_target_libs) - set(x_src_libs))]

    return { 'to_install': to_install, 'to_uninstall': to_remove} 