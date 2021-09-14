import CONFIG from './Config';
import AppUtil from './util/AppUtil';

let session_id = null;

const Request = {

    RAW: async function(endpoint, body){
        return request('', endpoint, body);
    },

    EXEC: async function(endpoint, body){
        endpoint = endpoint.replace('/exec', '');
        return request('/exec', endpoint, body);
    },

    GET: async function(endpoint){
        endpoint = '/exec' + endpoint;
        return await this.EXEC(endpoint, {});
    },

    BLOB: async function(endpoint, body){
        body['session_id'] = get_session_id();
        return await fetch(CONFIG.HOST + endpoint, {
            method: 'POST',
            headers: {
                'Accept': 'application/octet-stream',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        }).then(response => {
            return response.blob();
        })
    },

    STATUS: async function(endpoint){
        return request('/status', endpoint + '/get', {});
    },

    QUERY: async function(endpoint, body){
        return request('/query', endpoint, body);
    },
};

async function request(prefix, endpoint, body) {
    body['session_id'] = get_session_id();
    return await fetch(CONFIG.HOST + prefix + endpoint, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
    }).then(response => {
        if (response.status !== 200) {
            AppUtil.goTo('/' + response.status);
            return null;
        }
        return response.json();
    }).then(data => {
        return data;
    });
}

function get_session_id() {
    if (!session_id) {
        session_id = localStorage.getItem('sessionId');
    }
    return session_id;
}


export default Request;