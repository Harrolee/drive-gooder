import axios from "axios";

const credentials = {
  username: "",
  password: "",
};

export const storeLoginCredentials = (username: string, password: string) => {
  credentials.username = username;
  credentials.password = password;
};

const buildAuthorizationHeader = () => {
  const data = btoa(`${credentials.username}:${credentials.password}`);
  return `Basic ${data}`;
};

export const getSplit = async (text: string) => {
    const data = {
      text: text,
    };
    const response  = await axios.post(`${process.env.REACT_APP_API_ROOT}/split`, data, {
        headers: {
          "content-type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization": buildAuthorizationHeader()
        },
      }).catch((error) => {
        console.error(error);
      });

    console.log(response);
}

export const getTTS = (text: string, emotion: string, playbackSpeed: GLfloat) => {

}

export const ask = () => {

}

export const summarize = (text: string) => {

}
