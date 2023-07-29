import axios from "axios";
import { BACKEND_URL } from "./constants";

export const getSplit = (text: string) => {
    const formData = new FormData();
    formData.append("text", text);
    const data  = axios.post(`${BACKEND_URL}/split`, formData, {
        headers: {
          "content-type": "multipart/form-data",
          "Access-Control-Allow-Origin": "*",
        },
      }).catch((error) => {
        console.error(error);
      });
    console.log(data);
    console.log(JSON.stringify(data));
}

export const getTTS = (text: string, emotion: string, playbackSpeed: GLfloat) => {

}

export const ask = () => {

}

export const summerize = (text: string) => {

}
