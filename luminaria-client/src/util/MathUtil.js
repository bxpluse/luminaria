const FLOAT_REGEX = /^-?\d+(?:[.,]\d*?)?$/;

const MathUtil = {

    isPositiveInt: function(num){
        if (this.isInt(num)) {
            return num >= 0;
        }
        return false;
    },

    isPositiveFloat: function(num){
        if (this.isFloat(num)) {
            return num >= 0;
        }
        return false;
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