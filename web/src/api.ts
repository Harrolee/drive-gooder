import axios from "axios";

const credentials = {
    username: "",
    password: "",
};

export const storeLoginCredentials = (username: string, password: string) => {
    credentials.username = username;
    credentials.password = password;
};

const buildAuthorizationHeaderFromStoredCredentials = () => {
    return buildAuthorizationHeader(credentials.username, credentials.password);
};

const buildAuthorizationHeader = (username: string, password: string) => {
    const data = btoa(`${username}:${password}`);
    return `Basic ${data}`;
};

export const authenticate = async (username: string, password: string) => {
    return axios.post(`${process.env.REACT_APP_API_ROOT}/authenticate`, null, {
        headers: {
            "content-type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": buildAuthorizationHeader(username, password)
        },
    }).then(() => {
        return true;
    })
    .catch((error) => {
        console.error(error);
        return false;
    });
}


export const getSplit = async (text: string): Promise<string[]> => {
    const data = {
        text: text,
    };
    return axios.post(`${process.env.REACT_APP_API_ROOT}/split`, data, {
        headers: {
            "content-type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": buildAuthorizationHeaderFromStoredCredentials()
        },
    }).then((response) => {
        return response.data;
    })
    .catch((error) => {
        console.error(error);
    });
}

export const getTTS = (text: string, emotion: string, playbackSpeed: GLfloat) => {

}

export const ask = () => {

}

export const summarize = (text: string) => {

}
