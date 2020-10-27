import CONFIG from "./Config";

const Request = {
    POST_JSON: async function(endpoint, body){
        return await fetch(CONFIG.HOST + endpoint, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        }).then(response => {
            return response.json();
        }).then(data => {
            return data;
        });
    },

    GET_JSON: async function(endpoint){
        return await fetch(CONFIG.HOST + endpoint, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        }).then(response => {
            return response.json();
        }).then(data => {
            return data;
        });
    },

    GET_FILE: async function(endpoint, body){
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
};

export default Request;