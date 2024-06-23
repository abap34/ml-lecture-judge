import axios from 'axios';
import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const AuthRedirect = () => {
    const location = useLocation();

    useEffect(() => {
        const forwardRequest = async () => {
            try {
                const searchParams = new URLSearchParams(location.search);
                const params = {};
                for (let param of searchParams) {
                    params[param[0]] = param[1];
                }

                console.log('Forwarding request with params:', params);

                await axios.get(`${process.env.REACT_APP_API_URL}/auth`, { params });
            } catch (error) {
                console.error('Error forwarding request:', error);
            }
        };

        forwardRequest();
    }, [location]);

    return (
        <div>
            認証中...
        </div>
    );
};

export default AuthRedirect;
