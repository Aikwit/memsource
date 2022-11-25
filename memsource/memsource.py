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


    def get3(self, url, payload=None, params=None, headers=None):
        #url = "https://cloud.memsource.com/web/api2/v1/clients?name=AIKWIT"

        if not payload:
            payload={}

        if not params:
            params={}

        if not headers:
            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'ApiToken {self.auth_token}'
            }

            # to ne dela, ker potem pri generiranju targeta javi, da ni acceptable
            '''
            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'ApiToken {self.auth_token}'
            }
            '''
        else:
            headers["Authorization"] = f'ApiToken {self.auth_token}'

        #response = requests.request("GET", url, data=json.dumps(payload), params=json.dumps(params), headers=json.dumps(headers))
        response = requests.request("GET", url, data=json.dumps(payload), params=params, headers=headers)
        return response

    def post3(self, url, payload=None, params=None, headers=None):
        #url = "https://cloud.memsource.com/web/api2/v1/clients?name=AIKWIT"

        if not payload:
            payload={}

        if not params:
            params={}

        if not headers:
            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'ApiToken {self.auth_token}'
            }
            
        else:
            headers["Authorization"] = f'ApiToken {self.auth_token}'

        if "Content-Type" in headers and headers["Content-Type"] == "application/octet-stream":
            response = requests.request("POST", url, data=payload, params=params, headers=headers)
        else:

        #response = requests.request("POST", url, data=json.dumps(payload), params=json.dumps(params), headers=json.dumps(headers))
            response = requests.request("POST", url, data=json.dumps(payload), params=params, headers=headers)
        return response

    def delete3(self, url, payload=None, params=None, headers=None):

        if not payload:
            payload={}

        if not params:
            params={}

        if not headers:
            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'ApiToken {self.auth_token}'
            }
        else:
            headers["Authorization"] = f'ApiToken {self.auth_token}'

        resp = requests.delete(url, data=json.dumps(payload), params=params, headers=headers)
        return resp

    def put3(self, url, payload=None, params=None, headers=None):

        if not payload:
            payload={}

        if not params:
            params={}

        if not headers:
            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'ApiToken {self.auth_token}'
            }
        else:
            headers["Authorization"] = f'ApiToken {self.auth_token}'

        resp = requests.put(url, data=json.dumps(payload), params=params, headers=headers)
        return resp

    def patch3(self, url, payload=None, params=None, headers=None):

        if not payload:
            payload={}

        if not params:
            params={}

        if not headers:
            headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'ApiToken {self.auth_token}'
            }
        else:
            headers["Authorization"] = f'ApiToken {self.auth_token}'

        resp = requests.patch(url, data=json.dumps(payload), params=params, headers=headers)
        return resp


    #done
    def merge_pages(self, resp, req_str, payload=None, params=None, headers=None):
        result = []
        result.append(resp['content'])
        params = {}
        if resp['totalPages'] > 1:
            for i in range(1, resp['totalPages']):
                params['pageNumber'] = str(i)
                resp = self.get3(req_str, payload, params, headers)
                result.append(json.loads(resp.text)['content'])
        return result


    def get_lists(self, data_type, payload=None, params=None, headers=None):

        resp = self.get3(self.url + data_type, payload, params, headers)
        resp = json.loads(resp.text)
        return self.merge_pages(resp, self.url + data_type, payload, params, headers)

    #done
    def get_user_assigned_jobs(self, userId, payload=None, params=None, headers=None):
        req_str = self.url + 'users/' + str(userId) + '/jobs'
        resp = self.get3(req_str, payload, params, headers)
        resp = json.loads(resp.text)
        return self.merge_pages(resp, req_str, payload, params, headers)


    #done
    def change_job_status(self, projectUid, jobUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/' + str(projectUid) +'/jobs/' + str(jobUid) + '/setStatus'
        resp = self.post3(req_str, payload, params, headers)
        return resp
    #done
    def create_project(self, payload=None, params=None, headers=None):
        req_str = self.url + 'projects'
        resp = self.post3(req_str, payload, params, headers)
        return resp
    #done
    def create_client(self, payload=None, params=None, headers=None):
        req_str = self.url + 'clients'
        resp = self.post3(req_str, payload, params, headers)
        return resp

    def edit_client(self, clientUid, payload=None, params=None, headers=None):
        req_str = self.url + 'clients/' + str(clientUid)
        resp = self.put3(req_str, payload, params, headers)
        return resp

    def delete_project(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/' + projectUid
        resp = self.delete3(req_str, payload, params, headers)
        return resp

    #done
    def create_tm(self, payload=None, params=None, headers=None):
        req_str = self.url + 'transMemories'
        resp = self.post3(req_str, payload, params, headers)
        return resp

    def edit_tm(self, transMemoryUid, payload=None, params=None, headers=None):
        req_str = self.url + 'transMemories/' + str(transMemoryUid)
        resp = self.put3(req_str, payload, params, headers)
        return resp

    #done
    def create_tb(self, payload=None, params=None, headers=None):
        req_str = self.url + 'termBases'
        resp = self.post3(req_str, payload, params, headers)
        return resp

    def create_project_template(self, payload=None, params=None, headers=None):
        req_str = self.url + 'projectTemplates'
        resp = self.post3(req_str, payload, params, headers)
        return resp

    def add_translation_memory(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/' + projectUid +'/transMemories'
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        resp = self.put3(req_str, payload, params, headers)
        return resp

    def add_termbase(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/' + projectUid +'/termBases'
        resp = self.put3(req_str, payload, params, headers)
        return resp

    def export_translation_memory(self, transMemoryUid, payload=None, params=None, headers=None):
        req_str = self.url + 'transMemories/' + transMemoryUid +'/export'
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        #print(req_str)
        resp = self.post3(req_str, payload, params, headers)
        return resp

    #https://cloud.memsource.com/web/api2/v1/transMemories/extractCleaned
    def extract_cleaned_translation_memory(self, payload=None, params=None, headers=None):
        req_str = self.url + 'transMemories/extractCleaned'
        resp = self.post3(req_str, payload, params, headers)
        return resp

    def download_export(self, asyncRequestId, payload=None, params=None, headers=None):
        req_str = self.url + 'transMemories/downloadExport/' + asyncRequestId
        resp = self.get3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/transMemories/downloadCleaned/{asyncRequestId}
    def download_cleaned(self, asyncRequestId, payload=None, params=None, headers=None):
        req_str = self.url + 'transMemories/downloadCleaned/' + asyncRequestId
        resp = self.get3(req_str, payload, params, headers)
        return resp

    def list_pending_requests(self, payload=None, params=None, headers=None):
        req_str = self.url + 'async'
        resp = self.get3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/async/{asyncRequestId}
    def get_async_request(self, asyncRequestId, payload=None, params=None, headers=None):
        req_str = self.url + 'async/' + asyncRequestId
        resp = self.get3(req_str, payload, params, headers)
        return resp

    def get_translation_memory(self, tmUid, payload=None, params=None, headers=None):
        req_str = self.url + 'transMemories/' + str(tmUid)
        resp = self.get3(req_str, payload, params, headers)
        return resp

    def create_user(self, payload=None, params=None, headers=None):
        req_str = 'https://cloud.memsource.com/web/api2/v2/users'
        resp = self.post3(req_str, payload, params, headers)
        return resp

    def get_project_template(self, ptUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projectTemplates/' + str(ptUid)
        resp = self.get3(req_str, payload, params, headers)
        return resp

    def get_project_template_mt(self, ptUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projectTemplates/' + str(ptUid + '/mtSettings')
        resp = self.get3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v2/projects/applyTemplate/{templateUid}
    def create_project_from_template(self, templateUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/applyTemplate/' + templateUid
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        resp = self.post3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/sVoXknWR19Nc0klJyeS1nq/jobs?token=07rfgwfiF3sBnXTZFHSokp6tx0TWmYHfJOGMLdZhGzJiLGfQSaRr5qB3NLplZXbp1
    def create_job(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/' + projectUid + "/jobs"
        resp = self.post3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/references
    def add_reference_file(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/' + projectUid + "/references"
        resp = self.post3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/analyses/byLanguages
    def create_analyses_by_languages(self, payload=None, params=None, headers=None):
        req_str = req_str = self.url + 'analyses/byLanguages'
        resp = self.post3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}/targetFile
    def generate_target(self, projectUid, jobUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/' + str(projectUid) + '/jobs/' + str(jobUid) + '/targetFile'
        resp = self.get3(req_str, payload, params, headers)
        return resp
    
    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}/original
    def generate_original(self, projectUid, jobUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/' + str(projectUid) + '/jobs/' + str(jobUid) + '/original'
        resp = self.get3(req_str, payload, params, headers)
        return resp
    
    # https://cloud.memsource.com/web/api2/v2/projects/{projectUid}/jobs
    def list_jobs_by_project(self, projectUid, payload=None, params=None, headers=None):
        
        req_str = self.url + 'projects/' + str(projectUid) + '/jobs'
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        resp = self.get3(req_str, payload, params, headers)
        #print(resp.json())
        if resp.status_code == 200:
            if resp.json()["totalPages"] == 1:
                return [resp,]
            else:
                merged_resp = []
                for i in range(resp.json()["totalPages"]):
                    
                    req_str = self.url + 'projects/' + str(projectUid) + '/jobs'  + '?pageNumber=' + str(i)
                    req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
                    resp2 = self.get3(req_str, payload, params, headers)
                    merged_resp.append(resp2)
                return merged_resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}
    def get_project(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + "projects/" + projectUid
        resp = self.get3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings
    def edit_template_analysis(self, tempUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projectTemplates/' + tempUid + "/analyseSettings"
        resp = self.put3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projectTemplates/{projectTemplateUid}/analyseSettings
    def get_template_analysis(self, tempUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projectTemplates/' + tempUid + "/analyseSettings"
        resp = self.get3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/quotes
    def list_project_quotes(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + "projects/" + str(projectUid) + "/quotes"
        resp = self.get3(req_str, payload, params, headers)
        return resp

    def list_jobs(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + "projects/" + str(projectUid) + "/jobs"
        req_str = req_str.replace('web/api2/v1/', 'web/api2/v2/')
        resp = self.get3(req_str, payload, params, headers)
        return resp

    def list_projects(self, payload=None, params=None, headers=None):
        req_str = self.url + "projects"
        resp = self.get3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}/segments
    def get_segments(self, projectUid, jobUid, payload=None, params=None, headers=None):
        req_str = self.url + "projects/" + str(projectUid) + "/jobs/" + str(jobUid) + "/segments"
        resp = self.get3(req_str, payload, params, headers)
        return resp

    # https://cloud.memsource.com/web/api2/v1/projects/{projectUid}/jobs/{jobUid}
    def get_job(self, projectUid, jobUid, payload=None, params=None, headers=None):
        req_str = self.url + "projects/" + str(projectUid) + "/jobs/" + str(jobUid)
        resp = self.get3(req_str, payload, params, headers)
        return resp

    # {{baseUrl}}/api2/v1/projects/:projectUid/applyTemplate/:templateUid/assignProviders/forJobParts
    def assign_providers(self, projectUid, templateUid, payload=None, params=None, headers=None):
        req_str = self.url + "projects/" + str(projectUid) + "/applyTemplate/" + str(templateUid) + "/assignProviders/forJobParts"
        resp = self.post3(req_str, payload, params, headers)
        return resp

    def generate_bilingual_file(self, projectUid, payload=None, params=None, headers=None):
        resp = self.post3(self.url + 'projects/{}/jobs/bilingualFile'.format(projectUid), payload, params, headers)
        return resp

    def patch_project(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/{}'.format(projectUid)
        resp = self.patch3(req_str, payload, params, headers)
        return resp

    def add_target_languages(self, projectUid, payload=None, params=None, headers=None):
        req_str = self.url + 'projects/{}/targetLangs'.format(projectUid)
        resp = self.post3(req_str, payload, params, headers)
        return resp