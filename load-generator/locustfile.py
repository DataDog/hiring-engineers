from locust import HttpLocust, TaskSet, task, between

class UserBehaviour(TaskSet):

    @task(4)
    def index(self):
        self.client.get('/')

    @task(2)
    def apm_endpoint(self):
        self.client.get('/api/apm')

    @task(1)
    def trace_endpoint(self):
        self.client.get('/api/trace')

class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)
