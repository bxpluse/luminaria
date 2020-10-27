import React, {useEffect, useState} from 'react';
import {BrowserRouter as Router, Link, Route, Switch} from "react-router-dom";
import Home from "./pages/Home";
import LogViewer from "./apps/logviewer/LogViewer";
import Header from "./pages/Header";
import Updater from "./apps/updater/Updater";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Form from "react-bootstrap/Form";
import FormControl from "react-bootstrap/FormControl";
import RCStreamer from "./apps/rc-streamer/RCStreamer";
import Socket from "./components/Socket";
import Backup from './apps/backup/Backup';

function Navigation() {

    return (
        <React.Fragment>
            <Router>
                <Header/>
                <Socket/>
                <CustomNavBar/>
                <div className="content py-5 bg-light">
                    <Switch>
                        <Route path="/updater">
                            <Updater />
                        </Route>
                        <Route path="/logs">
                            <LogViewer />
                        </Route>
                        <Route path="/rc-streamer">
                            <RCStreamer />
                        </Route>
                        <Route path="/backup">
                            <Backup />
                        </Route>
                        <Route path="/">
                            <Home />
                        </Route>
                    </Switch>
                </div>
                <footer className="footer bg-light"/>
            </Router>
        </React.Fragment>
    );
}

function CustomNavBar() {

    const [fireworks, setFireworks] = useState({
        fire() {}
    });

    useEffect(() => {
        import('./components/Fireworks').then(Fireworks => {
            setFireworks(Fireworks);
        });
    }, []);

    return (
        <Navbar className={'custom-nav-bar navbar-expand-lg navbar-dark bg-dark'} bg="light" variant="light">
            <Link to="/">
                <Navbar.Brand>Home</Navbar.Brand>
            </Link>
            <Nav className="mr-auto">
                <Nav.Link
                    onClick={() => {
                        for(let i = 0; i < 6; i++){
                            setTimeout(
                                () => fireworks.fire(),
                                Math.random() * 750
                            );
                        }}
                }>Festival</Nav.Link>
            </Nav>
            <Form inline>
                <FormControl type="text" placeholder="Search" className="mr-sm-2" disabled={true}/>
            </Form>
        </Navbar>
    );
}


export default Navigation;