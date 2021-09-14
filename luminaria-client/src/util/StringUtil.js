const StringUtil = {
    capitalize: function (string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    },

    stripPeriod: function (string) {
        const lastChar = string[string.length - 1];
        if (lastChar === '.') {
            return string.slice(0, -1);
        }
        return string;
    },

    listToString: function (list, sep) {
        let result = '';
        for (let i = 0; i < list.length; i++) {
            result += list[i];
            if (i !== list.length - 1) {
                result += sep;
            }
        }
        return result
    },

    format: function (string, args) {
        for (let i = 0; i < args.length; i++)
            string = string.replace('{' + i + '}', args[i]);
        return string;
    }
};

export default StringUtil;