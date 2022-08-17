import requests
import json


class Memsource():
    url = 'https://cloud.memsource.com/web/api2/v1/'
    username = None
    password = None
    auth_token = None
    repository_path = None

    def __init__(self, username, password):
        self.username = username
        self.password = password
        print('Authenticating to Memsource as {} ... '.format(username), end='')
        self.auth_token = self.authenticate()
        if self.auth_token is not None:
            print('OK')
        else:
            print('ERROR')

    def authenticate(self):
        payload = dict()
        payload["userName"] = self.username
        payload["password"] = self.password
        resp = requests.post(self.url + 'auth/login', data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if resp.status_code != 200:
            return None
        resp = json.loads(resp.text)
        return resp['token']

    def get(self, url, pageNumber=None):
        if '?' in url:
            if pageNumber == None:
                resp = requests.get(url + '&token={}'.format(self.auth_token))
            else:
                resp = requests.get(url + '&token={}'.format(self.auth_token) + '&pageNumber=' + str(pageNumber))
        else:
            if pageNumber == None:
                resp = requests.get(url + '?token={}'.format(self.auth_token))
            else:
                resp = requests.get(url + '?token={}'.format(self.auth_token) + '&pageNumber=' + str(pageNumber))
        return resp

    def get2(self, url, params=None):
        if '?' in url:
            resp = requests.get(url + '&token={}'.format(self.auth_token), params)
        else:
            resp = requests.get(url + '?token={}'.format(self.auth_token), params)
        return resp

    def delete(self, url, projectUid):
        resp = requests.delete(url + projectUid + '?token={}'.format(self.auth_token))
        return resp

    def post(self, url, payload, headers={"Content-Type": "application/json"}):
        resp = requests.post(url + '?token={}'.format(self.auth_token), data=json.dumps(payload), headers=headers)
        return resp

    def post2(self, url, payload, headers={"Content-Type": "application/json"}):
        resp = requests.post(url + '?token={}'.format(self.auth_token), data=payload, headers=headers)
        return resp

    def put(self, url, payload):
        resp = requests.put(url + '?token={}'.format(self.auth_token), data=json.dumps(payload), headers={"Content-Type": "application/json"})
        return resp

    def merge_pages(self, resp, req_str, payload):
        result = []
        result.append(resp['content'])
        if resp['totalPages'] > 1:
            for i in range(1, resp['totalPages']):
                payload['pageNumber'] = str(i)
                resp = self.get2(req_str, payload)
                result.append(json.loads(resp.text)['content'])
        return result


    def get_lists(self, data_type, payload):

        resp = self.get2(self.url + data_type, payload)
        resp = json.loads(resp.text)
        return self.merge_pages(resp, self.url + data_type, payload)

    def get_user_assigned_jobs(self, userId, payload):
        req_str = self.url + 'users/' + str(userId) + '/jobs'
        resp = self.get2(req_str, payload)
        resp = json.loads(resp.text)
        return self.merge_pages(resp, req_str, payload)

    def change_job_status(self, projectUid, jobUid, payload):
        req_str = self.url + 'projects/' + str(projectUid) +'/jobs/' + str(jobUid) + '/setStatus'
        resp = self.post(req_str, payload)
        return resp

    def create_project(self, payload):
        req_str = self.url + 'projects'
        resp = self.post(req_str, payload)
        return resp

    def create_client(self, payload):
        req_str = self.url + 'clients'
        resp = self.post(req_str, payload)
        return resp

    def edit_client(self, clientUid, payload):
        req_str = self.url + 'clients/' + str(clientUid)
        resp = self.put(req_str, payload)
        return resp

    def delete_project(self, projectUid):
        req_str = self.url + 'projects/'
        resp = self.delete(req_str, projectUid)
        return resp

    #def create_job(self, projectUid, payload):
    #    req_str = self.url + 'projects/' + str(projectUid) +'/jobs'
    #    resp = self.post(req_str, payload)
    #    return resp

    def create_tm(self, payload):
        req_str = self.url + 'transMemories'
        resp = self.post(req_str, payload)
        return resp

    def edit_tm(self, transMemoryUid, payload):
        req_str = self.url + 'transMemories/' + str(transMemoryUid)
        resp = self.put(req_str, payload)
        return resp

    def create_tb(self, payload):
        req_str = self.url + 'termBases'
        resp = self.post(req_str, payload)
        return resp

    def create_project_template(self, payload):
        req_str = self.url + 'projectTemplates'
        resp = self.post(req_str, payload)
        return resp

    def add_translation_memory(self, projectUid, payload):
        req_str = self.url + 'projects/' + projectUid +'/transMemories'
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        resp = self.put(req_str, payload)
        return resp

    def add_termbase(self, projectUid, payload):
        req_str = self.url + 'projects/' + projectUid +'/termBases'
        resp = self.put(req_str, payload)
        return resp

    def export_translation_memory(self, transMemoryUid, payload):
        req_str = self.url + 'transMemories/' + transMemoryUid +'/export'
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        #print(req_str)
        resp = self.post(req_str, payload)
        return resp

    #https://cloud.memsource.com/web/api2/v1/transMemories/extractCleaned
    def extract_cleaned_translation_memory(self, payload):
        req_str = self.url + 'transMemories/extractCleaned'
        resp = self.post(req_str, payload)
        return resp

    def download_export(self, asyncRequestId, payload):
        req_str = self.url + 'transMemories/downloadExport/' + asyncRequestId
        resp = self.get2(req_str, payload)
        return resp

    # https://cloud.memsource.com/web/api2/v1/transMemories/downloadCleaned/{asyncRequestId}
    def download_cleaned(self, asyncRequestId, payload):
        req_str = self.url + 'transMemories/downloadCleaned/' + asyncRequestId
        resp = self.get2(req_str, payload)
        return resp

    def list_pending_requests(self):
        req_str = self.url + 'async'
        resp = self.get2(req_str)
        return resp

    # https://cloud.memsource.com/web/api2/v1/async/{asyncRequestId}
    def get_async_request(self, asyncRequestId):
        req_str = self.url + 'async/' + asyncRequestId
        resp = self.get2(req_str)
        return resp

    def get_translation_memory(self, tmUid):
        req_str = self.url + 'transMemories/' + str(tmUid)
        resp = self.get2(req_str)
        return resp

    def create_user(self, payload):
        req_str = 'https://cloud.memsource.com/web/api2/v2/users'
        resp = self.post(req_str, payload)
        return resp

    def get_project_template(self, ptUid):
        req_str = self.url + 'projectTemplates/' + str(ptUid)
        resp = self.get2(req_str)
        return resp

    def get_project_template_mt(self, ptUid):
        req_str = self.url + 'projectTemplates/' + str(ptUid + '/mtSettings')
        resp = self.get2(req_str)
        return resp

    # https://cloud.memsource.com/web/api2/v2/projects/applyTemplate/{templateUid}
    def create_project_from_template(self, templateUid, payload):
        req_str = self.url + 'projects/applyTemplate/' + templateUid
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        resp = self.post(req_str, payload)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/sVoXknWR19Nc0klJyeS1nq/jobs?token=07rfgwfiF3sBnXTZFHSokp6tx0TWmYHfJOGMLdZhGzJiLGfQSaRr5qB3NLplZXbp1
    def create_job(self, projectUid, payload, headers):
        req_str = self.url + 'projects/' + projectUid + "/jobs"
        resp = self.post2(req_str, payload, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/references
    def add_reference_file(self, projectUid, payload, headers):
        req_str = self.url + 'projects/' + projectUid + "/references"
        resp = self.post2(req_str, payload, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/analyses/byLanguages
    def create_analyses_by_languages(self, payload):
        req_str = req_str = self.url + 'analyses/byLanguages'
        resp = self.post(req_str, payload)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}/targetFile
    def generate_target(self, projectUid, jobUid):
        req_str = self.url + 'projects/' + str(projectUid) + '/jobs/' + str(jobUid) + '/targetFile'
        resp = self.get(req_str)
        return resp
    
    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}/original
    def generate_original(self, projectUid, jobUid):
        req_str = self.url + 'projects/' + str(projectUid) + '/jobs/' + str(jobUid) + '/original'
        resp = self.get(req_str)
        return resp
    
    # https://cloud.memsource.com/web/api2/v2/projects/{projectUid}/jobs
    def list_jobs_by_project(self, projectUid, workflowLevel):
        params = {
            "workflowLevel": workflowLevel
        }
        req_str = self.url + 'projects/' + str(projectUid) + '/jobs'
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        resp = self.get2(req_str, params)
        #print(resp.json())
        if resp.status_code == 200:
            if resp.json()["totalPages"] == 1:
                return [resp,]
            else:
                merged_resp = []
                for i in range(resp.json()["totalPages"]):
                    
                    req_str = self.url + 'projects/' + str(projectUid) + '/jobs'  + '?pageNumber=' + str(i)
                    req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
                    resp2 = self.get2(req_str, params)
                    merged_resp.append(resp2)
                return merged_resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}
    def get_project(self, projectUid):
        req_str = self.url + "projects/" + projectUid
        resp = self.get(req_str)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings
    def edit_template_analysis(self, tempUid, payload):
        req_str = self.url + 'projectTemplates/' + tempUid + "/analyseSettings"
        resp = self.put(req_str, payload)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings
    def get_template_analysis(self, tempUid):
        req_str = self.url + 'projectTemplates/' + tempUid + "/analyseSettings"
        resp = self.get(req_str)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/quotes
    def list_project_quotes(self, projectUid):
        req_str = self.url + "projects/" + str(projectUid) + "/quotes"
        resp = self.get(req_str)
        return resp

    def list_jobs(self, projectUid, payload):
        req_str = self.url + "projects/" + str(projectUid) + "/jobs"
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        resp = self.get(req_str, payload)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}/segments
    def get_segments(self, projectUid, jobUid, payload):
        req_str = self.url + "projects/" + str(projectUid) + "/jobs/" + str(jobUid) + "/segments"
        resp = self.get2(req_str, payload)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}
    def get_job(self, projectUid, jobUid):
        req_str = self.url + "projects/" + str(projectUid) + "/jobs/" + str(jobUid)
        resp = self.get(req_str)
        return resp
