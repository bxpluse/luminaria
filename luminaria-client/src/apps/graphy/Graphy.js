import React, {useState} from 'react';
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form';
import Jumbotron from 'react-bootstrap/Jumbotron';
import MyButton from '../../components/MyButton';


function Graphy() {
    return (
        <Container>
            <h2>Graphy</h2>
            <br/>
            <GraphJumbotron
                title='Mentions'
                body='Get mentions of a symbol'
                params={'api=getMentionsGraph'}
            />
        </Container>
    );
}

function GraphJumbotron(props) {

    const [symbol, setSymbol] = useState('');

    return(
        <Jumbotron>
            <h3>{props.title}</h3>
            <p>{props.body}</p>
            <Form>
                <Form.Group>
                    <Form.Control style={{width: '20%'}} type="text" placeholder="Symbol" value={symbol}
                                  onChange={e => setSymbol(e.target.value)} />
                </Form.Group>
            </Form>
            <MyButton text='Get' onClick={() => {
                if (symbol !== '') {
                    openGraph(props.params + '&symbol=' + symbol.toUpperCase())
                    setSymbol('');
                }
            }}/>
        </Jumbotron>
    )
}

function openGraph(params) {
    window.open('/graph?' + params, '_blank', 'noopener,noreferrer')
}


export default Graphy;