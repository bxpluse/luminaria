import React, {useEffect} from 'react';
import { ToastContainer, toast } from 'react-toastify';
import openSocket  from "socket.io-client";
import 'react-toastify/dist/ReactToastify.css';
import CONFIG from "../Config";


function Socket() {

    useEffect(()=>{

        const socket = openSocket.connect(CONFIG.HOST);

        socket.on('toast-message', (data) => {
            const message = data.message;
            const options = {
                position: "top-right",
                autoClose: data.duration * 1000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
            };

            switch(data.variant) {
                case 'success':
                    toast.success(message, options);
                    break;
                case 'warning':
                    toast.warning(message, options);
                    break;
                case 'error':
                    toast.error(message, options);
                    break;
                case 'dark':
                    toast.dark(message, options);
                    break;
                default:
                    toast.info(message, options);
            }
        });


        // socket.on('toast-status', (data) => {
        //     console.log(data);
        // });

    }, []);

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