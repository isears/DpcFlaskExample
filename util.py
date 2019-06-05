import requests
import time
import json
import threading


class DPCDataFetcher():

    in_memory_datastore = []

    def __init__(self, provider_id):
        self.provider_id = provider_id
        self.internal_thread = threading.Thread(target=self._fetchData, args=())
        self.running = False
        self.error_msg = ''


    def update_state(self):
        if not self.running:
            pass
        elif self.internal_thread.isAlive():
            pass
        else:
            self.internal_thread.join()
            self.running = False
            self.internal_thread = threading.Thread(target=self._fetchData, args=()) # Get ready for next run

        return {
                'running': self.running,
                'error_msg': self.error_msg,
                'provider_id': self.provider_id
            }

    def start_request(self):
        self.running = True
        self.error_msg = ''
        self.internal_thread.start()
        

    def _fetchData(self):
        ret, err = self._bulk_export_patients()

        if err == None:
            self.in_memory_datastore.clear()
            for entry in ret:
                self.in_memory_datastore.append(entry)
        else:
            print('Exception while communicating with DPC')
            self.error_msg = err



    def _bulk_export_patients(self):
        try:
            sess = requests.session()

            # Kickstart job
            resp = sess.get('http://localhost:3002/v1/Group/{}/$export?_type=Patient'.format(self.provider_id))

            assert(resp.status_code == 204), 'Expected 204 on initial request, but got {}'.format(resp.status_code)  # TODO: more specific error handling

            next_hop = resp.headers['Content-Location']

            while True:
                resp = sess.get(next_hop)

                assert (resp.status_code == 202 or resp.status_code == 200), 'Expected 202 or 200, but got {}'.format(resp.status_code)

                if resp.status_code == 202:  # Waiting for job to complete...
                    time.sleep(5)  # TODO: Make this a config option
                    pass
                elif resp.status_code == 200:  # Job completed successfully
                    next_hop = json.loads(resp.text)['output'][0]['url']  # TODO: more specific data retrieval

                    ret_raw = sess.get(next_hop).text

                    return [json.loads(x) for x in ret_raw.split()], None

                else:  # Some kind of error condition
                    print('This shouldn\'t happen...')
                    break
        except Exception as ex:
            return [], str(ex)


if __name__ == '__main__':
    dataFetcher = DPCDataFetcher('8D80925A-027E-43DD-8AED-9A501CC4CD91')
    patients = dataFetcher._bulk_export_patients()

    for patient in patients:
        print(patient)
