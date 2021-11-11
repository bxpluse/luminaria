const FLOAT_REGEX = /^-?\d+(?:[.,]\d*?)?$/;

const MathUtil = {

    isPositiveInt: function(num){
        return this.isInt(num) >= 0;
    },

    isInt: function(num){
        if (!FLOAT_REGEX.test(num)) {
            return false;
        }
        if (typeof num === 'string') {
            num = parseFloat(num);
        }
        return Number.isInteger(num);
    },

    isFloat: function(num){
        if (!FLOAT_REGEX.test(num)) {
            return false;
        }
        num = parseFloat(num);
        return !isNaN(num);
    },
};

export default MathUtil;