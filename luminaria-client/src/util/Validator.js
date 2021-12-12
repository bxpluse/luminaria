import MathUtil from './MathUtil';
import ClientSideException from '../exceptions/ClientSideException';


const Validator = {

    validateNonEmptyString: function (val) {
        if (!val || val.length === 0) {
            throw ClientSideException(`Input (${val}) should be a non-empty string`);
        }
    },

    validatePositiveInt: function (val) {
        if (!MathUtil.isPositiveInt(val)) {
            throw ClientSideException(`Input (${val}) should be a positive integer`);
        }
    },

    validatePositiveFloat: function (val) {
        if (!MathUtil.isPositiveFloat(val)) {
            throw ClientSideException(`Input (${val}) should be a positive float`);
        }
    },
};


export default Validator;