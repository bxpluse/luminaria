import React, {useEffect} from "react";
import Container from 'react-bootstrap/Container';
import MyButton from "../../components/MyButton";
import Request from '../../Requests';


function Syscmd() {

    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    return (
        <Container>
            <SimpleRequestBtn text='Refresh Apps' endpoint='/syscmd/refresh-apps'/>
            <SimpleRequestBtn text='Refresh Config' endpoint='/syscmd/refresh-config'/>
        </Container>
    );
}

function SimpleRequestBtn(props) {
    return (
        <Container>
            <MyButton text={props.text} onClick={() => {
                Request.GET(props.endpoint).then();
            }}/>
            <br/><br/>
        </Container>
    );
}


export default Syscmd;