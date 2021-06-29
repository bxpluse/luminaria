const MathUtil = {
    isPositiveInt: function(num){
        if (Number.isInteger(num)){
            if (num > 0){
                return true;
            }
        }
        return false;
    },
};

export default MathUtil;