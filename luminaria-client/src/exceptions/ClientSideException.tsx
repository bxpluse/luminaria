import {toast, ToastOptions} from 'react-toastify';


function ClientSideException(message: string, duration: number = 2.5): any {
    console.log(`CSE: ${message}`);
    const options: ToastOptions = {
        position: 'top-right',
        autoClose: duration * 1000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
    };
    toast.error(`CSE: ${message}`, options);
}


export default ClientSideException;