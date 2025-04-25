'use client'

import axios from 'axios';

const getBaseUrl = () => {
    let url;
    switch(process.env.NODE_ENV) {
        case 'production':
        url = 'http://localhost:8000';
        break;
        case 'development':
        default:
        url = 'http://localhost:8000';
    }

    return url;
}

export const axiosHttp = axios.create({
    baseURL: getBaseUrl(),
});

export const axiosGet = (url, ok_callback, fail_callback) => {
    return axiosHttp.get(url)
        .then(function (response) {
            if (response.status === 200) {
                ok_callback(response.data);
            } else {
                fail_callback(response.data);
            }
        })
        .catch(function (error) {
            console.log("HTTP error", error);
            fail_callback(error)
        })
}
