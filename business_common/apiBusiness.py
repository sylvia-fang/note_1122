import requests
from common.read_yml import ReadYaml


class ApiBusiness:
    rY = ReadYaml()
    env_config = rY.env_yaml()
    host = env_config['host']

    def clear_file_members(self, file_id):
        url = self.host + '/clear'
        data = {
            'file_id': file_id
        }
        res = requests.delete(url=url, json=data)
        if res.status_code != 200:
            return False
        else:
            return True
