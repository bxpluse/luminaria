const DictUtil = {
    sort: function(dict){
        return Object.keys(dict).sort().reduce(
            (obj, key) => {
                obj[key] = dict[key];
                return obj;
            }, {}
        );
    },
};


export default DictUtil;