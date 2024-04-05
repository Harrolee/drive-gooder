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
  return axios
    .post(`${process.env.REACT_APP_API_ROOT}/authenticate`, null, {
      headers: {
        "content-type": "application/json",
        "Access-Control-Allow-Origin": "*",
        Authorization: buildAuthorizationHeader(username, password),
      },
    })
    .then(() => {
      return true;
    })
    .catch((error) => {
      console.error(error);
      return false;
    });
};

export const oauth = async () => {
  return axios
    .get(`${process.env.REACT_APP_API_ROOT}/login`, {
      headers: {
        "content-type": "application/json",
        "Access-Control-Allow-Origin": "*",
        Authorization: buildAuthorizationHeaderFromStoredCredentials(),
      },
    })
    .then((response) => {
      return response;
    });
};

export const getSplit = async (text: string): Promise<string[]> => {
  const data = {
    text: text,
  };

  return fetch(`${process.env.REACT_APP_API_ROOT}/split`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "Access-Control-Allow-Origin": "*",
      Authorization: buildAuthorizationHeaderFromStoredCredentials(),
      responseType: "blob",
    },
    body: JSON.stringify(data),
  })
    .then(async (response) => {
      return (await response.json()) as string[];
    })
    .catch((error) => {
      console.error(error);
      return Promise.reject();
    });
};

export const getUserInfo = async () => {
  return await fetch(`${process.env.REACT_APP_API_ROOT}/me`, {
    method: "GET",
    headers: {
      "content-type": "application/json",
      credentials: "include",
    },
  })
    .then(async (response) => {
      if (!response.ok) {
        return { authenticated: "false" };
      }
      return await response.json();
    })
    .catch((error) => {
      console.log("error in the getUserInfo request");
      console.error(error);
      return Promise.reject();
    });
};
export const readText = (text: string, emotion: string, speed: number) => {
  const data = {
    text,
    emotion,
    speed,
  };

  return fetch(`${process.env.REACT_APP_API_ROOT}/read`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "Access-Control-Allow-Origin": "*",
      Authorization: buildAuthorizationHeaderFromStoredCredentials(),
      responseType: "blob",
    },
    body: JSON.stringify(data),
  })
    .then(async (response) => {
      return await response.blob();
    })
    .catch((error) => {
      console.error(error);
      return Promise.reject();
    });
};

export const ask = (
  audio: Blob,
  text: string,
  emotion: string,
  speed: number
) => {
  const formData = new FormData();
  formData.set("text", text);
  formData.set("emotion", emotion);
  formData.set("speed", speed.toString());
  formData.set("question.wav", audio);

  return fetch(`${process.env.REACT_APP_API_ROOT}/ask`, {
    method: "POST",
    headers: {
      "Access-Control-Allow-Origin": "*",
      Authorization: buildAuthorizationHeaderFromStoredCredentials(),
      responseType: "blob",
    },
    body: formData,
  })
    .then(async (response) => {
      return await response.blob();
    })
    .catch((error) => {
      console.error(error);
      return Promise.reject();
    });
};

export const summarize = (
  text: string,
  emotion: string,
  speed: number
): Promise<Blob> => {
  const data = {
    text,
    emotion,
    speed,
  };

  return fetch(`${process.env.REACT_APP_API_ROOT}/summarize`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "Access-Control-Allow-Origin": "*",
      Authorization: buildAuthorizationHeaderFromStoredCredentials(),
      responseType: "blob",
    },
    body: JSON.stringify(data),
  })
    .then(async (response) => {
      return await response.blob();
    })
    .catch((error) => {
      console.error(error);
      return Promise.reject();
    });
};
