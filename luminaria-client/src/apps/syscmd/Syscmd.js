import React, {useEffect} from "react";
import Container from 'react-bootstrap/Container';
import MyButton from "../../components/MyButton";
import Request from "../../Requests";


function Syscmd() {

    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    return (
        <Container>
            <MyButton text='Refresh Apps' onClick={() => {
                Request.GET_JSON('/get/syscmd/refresh-apps').then();
            }}/>
            <br/><br/>
        </Container>
    );
}


export default Syscmd;