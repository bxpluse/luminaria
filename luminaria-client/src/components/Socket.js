import React from 'react';
import { ToastContainer, toast } from 'react-toastify';
import openSocket  from "socket.io-client";
import 'react-toastify/dist/ReactToastify.css';
import CONFIG from "../Config";


function Socket() {

    const socket = openSocket.connect(CONFIG.HOST);

    socket.on('toast-message', (data) => {
        toast.warn(data.message, {
            position: "top-right",
            autoClose: 8000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
        });
    });

    //socket.on('toast-status', (data) => {
    //    console.log(data);
    //});

    return (
        <div>
            <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
            />
        </div>
    );
}


export default Socket;