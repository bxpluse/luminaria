import React from 'react';

class Test extends React.Component {

    constructor(props) {
        super(props);
    }

    componentDidMount() {

    }

    activateLasers() {
        fetch('http:/host:port/test', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                order: 'fire'
            })
        }).then(response => {
            return response.json();
        }).then(data => {
            console.log(data.message)
        })
    }

    render() {

        return (
            <React.Fragment>
                <p>TEST COMPONENT</p>
                <button onClick={this.activateLasers}>  Activate Lasers
                </button>
            </React.Fragment>
        );
    }
}


export default Test;