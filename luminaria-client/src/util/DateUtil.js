import moment from 'moment';


const DateUtil = {
    getCurrentDate: function(){
        // Return string in yyyy-mm-dd format
        let today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        const yyyy = today.getFullYear();
        today = yyyy + '-' + mm + '-' + dd;
        return today;
    },

    parse: function(date_str){
        return moment(date_str).format('lll')
    },
};

export default DateUtil;