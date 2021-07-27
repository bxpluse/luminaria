const AppUtil = {
    getCurrentApp: function() {
        const arr = window.location.href.split('/');
        return arr[arr.length - 1].split('?')[0]
    },

    getUrlParams: function () {
        const arr = window.location.href.split('/');
        const paramString = arr[arr.length - 1].split('?')[1];
        const keyValuePairs = paramString.split('&');
        let params = {};
        for(let i = 0; i < keyValuePairs.length; i++) {
            const keyValueArr = keyValuePairs[i].split('=');
            params[keyValueArr[0]] = keyValueArr[1];
        }
        return params;
    },

    isDevEnv: function () {
        return process.env.NODE_ENV === 'development';
    },
};


export default AppUtil;